import enum
from datetime import datetime
from inspect import isclass
from typing import Annotated, Type, TypeVar, get_args, get_origin

import sqlalchemy as sa
from sqlalchemy import Select, orm, select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql.sqltypes import _type_map as SQL_TYPES
from mlib.logger import log

T = TypeVar("T", bound=Type["Base"])
V = TypeVar("V")


class ASession(AsyncSession):
    async def query(self, statement: Select[V], index: int = 0, **kwargs) -> V:
        r = await self.execute(statement, **kwargs)
        return r.scalars(index).all()

    async def first(self, statement: Select[V], **kwargs) -> V:
        r = await self.execute(statement, **kwargs)
        return r.scalar()


class Base(orm.MappedAsDataclass, orm.DeclarativeBase):
    @orm.declared_attr
    def __tablename__(cls):
        return cls.__name__

    @classmethod
    async def fetch_or_add(cls: T, session: ASession, **kwargs) -> T:
        """Fetch from database or create new object"""
        if row := await session.scalar(select(cls).filter_by(**kwargs)):
            return row
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    async def filter(cls: T, session: ASession, *args, **kwargs) -> list[T]:
        """:param kwargs: Column = Value"""
        result = await session.scalars(select(cls).filter(*args).filter_by(**kwargs))
        return result.all()

    @classmethod
    async def fetch_or_add_multiple(cls: T, session: ASession, *ids: int) -> list[T]:
        objects = []
        for id in ids:
            objects.append(await cls.fetch_or_add(session, id=id))
        for obj in objects:
            session.add(obj)
        return objects

    @classmethod
    async def by_id(cls: T, session: ASession, id: int) -> T | None:
        return await session.scalar(select(cls).filter_by(id=id))

    @classmethod
    async def by_name(cls: T, session: ASession, name: str) -> T | None:
        return await session.scalar(select(cls).filter_by(name=name))

    @classmethod
    async def get(cls: T, session: ASession, *args) -> T | None:
        return await session.scalar(select(cls).filter(*args))


class MappedWrapper:
    def __init_subclass__(cls, **kwargs) -> None:
        for annotation, _type in cls.__annotations__.items():
            if get_origin(_type) is not orm.Mapped:
                cls.__annotations__[annotation] = orm.Mapped[_type]

        return super().__init_subclass__(**kwargs)


class ImperativeTable:
    def __init_subclass__(cls, schema: str = "public", **kwargs) -> None:
        columns, nullable = [], False

        for attribute, annotation in cls.__annotations__.items():
            if base_types := get_args(annotation):
                if type(None) in base_types:
                    nullable = True
                annotation = base_types[0]
            value = cls.__dict__.get(attribute)
            if type(value) is orm.MappedColumn:
                columns.append(
                    sa.Column(
                        attribute,
                        SQL_TYPES.get(annotation),
                        nullable=nullable,
                        primary_key=value.column.primary_key,
                    )
                )
                cls.__delattr__(cls, attribute)
            else:
                columns.append(sa.Column(attribute, SQL_TYPES.get(annotation), nullable=nullable))

        cls.__annotations__ = {}
        cls.__table__ = sa.Table(cls.__tablename__, Base.metadata, schema=schema, *columns)

        return super().__init_subclass__(**kwargs)


auto_int_pk = Annotated[int, orm.mapped_column(primary_key=True, autoincrement=True)]
unique_name = Annotated[str, orm.mapped_column(sa.String, unique=True, nullable=False)]

ts_default = Annotated[datetime, orm.mapped_column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())]
ts_update = Annotated[
    datetime, orm.mapped_column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
]


class ID(orm.MappedAsDataclass):
    """Mixin adding autoincrementing integer ID"""

    id: orm.Mapped[auto_int_pk] = orm.mapped_column(init=False)


class Default(ID, orm.MappedAsDataclass):
    """Mixin adding unique name with ID"""

    name: orm.Mapped[unique_name] = orm.mapped_column()


class File(ID, orm.MappedAsDataclass):
    """Mixin adding filename with ID"""

    filename: orm.Mapped[str | None] = orm.mapped_column()


class Timestamp(orm.MappedAsDataclass):
    """Mixin adding server default timestamp with timezone (if empty)"""

    timestamp: orm.Mapped[ts_default] = orm.mapped_column(kw_only=True, default=None)


class TimestampUpdate(orm.MappedAsDataclass):
    """Mixin adding timestamp that updates on update with server default with timezone (if empty)"""

    timestamp: orm.Mapped[ts_update] = orm.mapped_column(kw_only=True, default=None)


async def extend_enums(session: async_sessionmaker[ASession], engine: Engine, module):
    """Extends existing DB Enum with new values from Coded Enum"""
    s = session()
    for _class in vars(module).values():
        if isclass(_class) and issubclass(_class, enum.Enum) and len(_class.__members__) > 0:
            try:
                r = await s.execute(
                    sa.text("SELECT * FROM unnest(enum_range(NULL::{}))".format(_class.__name__.lower()))
                )
                r = r.scalars().all()
            except ProgrammingError as ex:
                log.warning("Unnesting enum %s failed", _class.__name__)
                await s.rollback()
                continue
            new_members = []
            for member in _class.__members__.keys():
                if hasattr(_class, "get"):
                    member = _class.get(member)
                    member = member.name
                if member not in r:
                    new_members.append(member)
            if new_members != []:
                for member in new_members:
                    log.info("Extending %s with value %s", _class.__name__, member)
                    await s.execute(sa.text("ALTER TYPE {} ADD VALUE '{}'".format(_class.__name__.lower(), member)))
                await s.commit()
    await s.close()


class SQL:
    """Synchronous SQLAlchemy client. Creates engine and sessionmaker"""

    def __init__(
        self,
        db: str = "postgresql",
        user: str = "postgres",
        password: str = "postgres",
        location: str = None,
        port: int = 5432,
        name: str = "db",
        echo: bool = True,
        *,
        url: str = None,
        **kwargs,
    ):
        try:
            url = url or self.build_url(name, db, user, password, location, port)
            self._create_engine(url, echo=echo, **kwargs)
        except ConnectionError as ex:
            log.exception("Connecting to Remote DB failed! Falling back to local SQLite", exc_info=ex)
            self._create_engine(self.build_url + ".db", echo=echo)
        self._create_sessionmaker()

    def build_url(
        self, name: str, db: str = "sqlite", user: str = None, password: str = None, host: str = None, port: int = None
    ) -> str:
        """Builds connection URL"""
        url = ""
        if user:
            url += user
        if password:
            url += f":{password}"
        if host:
            url += f"@{host}"
        if port:
            url += f":{port}"
        return f"{db}://{url}/{name}"

    def _create_engine(self, url: str, echo: bool = True, **kwargs):
        """Creates synchronous engine"""
        self._engine = sa.create_engine(url, echo=echo, **kwargs)

    def _create_sessionmaker(self):
        """Creates synchronous session factory"""
        self._session = orm.sessionmaker(bind=self._engine)

    def Session(self):
        """Creates new session"""
        return self._session()

    def session(self):
        """Creates new session"""
        return self._session()

    def create_tables(self, base: Base = Base):
        """Creates tables synchronously"""
        base.metadata.create_all(self._engine)

    def drop_tables(self, base: Base = Base):
        """Drops tables synchronously"""
        base.metadata.drop_all(self._engine)

    def merge(self, mapping: T):
        with self.session.begin() as s:
            s.merge(mapping)

    def add(self, mapping: T):
        with self.session.begin() as s:
            s.add(mapping)

    def delete(self, mapping: T):
        with self.session.begin() as s:
            s.delete(mapping)

    def merge_or_add(self, queried_result: T, mapping: T):
        if queried_result:
            return self.merge(mapping)
        return self.add(mapping)

    def extend_enums(self, module):
        return extend_enums(self.session(), self._engine, module)


class AsyncSQL(SQL):
    """Asynchronous SQLAlchemy client. Creates async engine and async sessionmaker"""

    def _create_engine(self, url: str, echo: bool = True, **kwargs):
        """Creates asynchronous engine"""
        self._engine = create_async_engine(url, echo=echo, **kwargs)

    def _create_sessionmaker(self):
        """Creates asynchronous session factory"""
        self.session = async_sessionmaker(bind=self._engine, class_=ASession)

    async def create_tables(self, base: Base = Base):
        """Creates tables asynchronously. To be used with await"""
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def drop_tables(self, base: Base = Base):
        """Drops tables asynchronously. To be used with await"""
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)

    async def merge(self, mapping: T):
        async with self.session.begin() as s:
            s.merge(mapping)

    async def add(self, mapping: T):
        async with self.session.begin() as s:
            s.add(mapping)

    async def delete(self, mapping: T):
        async with self.session.begin() as s:
            s.delete(mapping)

    async def merge_or_add(self, queried_result: T | None, mapping: T):
        if queried_result:
            return await self.merge(mapping)
        return await self.add(mapping)

    async def extend_enums(self, session: ASession, module):
        return await extend_enums(session, self._engine, module)
