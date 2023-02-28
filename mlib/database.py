from datetime import datetime
from typing import Annotated

import sqlalchemy as sa

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine import Engine


class Base(orm.MappedAsDataclass, orm.DeclarativeBase):
    @orm.declared_attr
    def __tablename__(cls):
        return cls.__name__



class MappedWrapper:
    def __init_subclass__(cls, **kwargs) -> None:
        for annotation, _type in cls.__annotations__.items():
            if get_origin(_type) is not orm.Mapped:
                cls.__annotations__[annotation] = orm.Mapped[_type]

        return super().__init_subclass__(**kwargs)


auto_int_pk = Annotated[int, orm.mapped_column(primary_key=True, autoincrement=True)]
unique_name = Annotated[str, orm.mapped_column(sa.String, unique=True, nullable=False)]

ts_default = Annotated[datetime, orm.mapped_column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now())]
ts_update = Annotated[
    datetime, orm.mapped_column(sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
]


class ID:
    """Mixin adding autoincrementing integer ID"""

    id: auto_int_pk


class Default(ID):
    """Mixin adding unique name with ID"""

    name: unique_name


class File(ID):
    """Mixin adding filename with ID"""

    filename: str


class Timestamp:
    """Mixin adding server default timestamp with timezone (if empty)"""

    timestamp: ts_default


class TimestampUpdate:
    """Mixin adding timestamp that updates on update with server default with timezone (if empty"""

    timestamp: ts_update


def extend_enums(session: orm.Session, engine: Engine, module):
    """Extends existing DB Enum with new values from Coded Enum"""
    import enum
    from inspect import isclass

    with session.begin() as s:
        for _class in vars(module).values():
            if isclass(_class) and issubclass(_class, enum.Enum) and len(_class.__members__) > 0:
                try:
                    r = s.query(sa.text("unnest(enum_range(NULL::{}))".format(_class.__name__.lower()))).all()
                except Exception as ex:
                    continue
                r = [j for i in r for j in i]
                new_members = []
                for member in _class.__members__.keys():
                    if member not in r:
                        new_members.append(member)
                if new_members != []:
                    with engine.connect() as con:
                        from .logger import log

                        for member in new_members:
                            log.info("Extending %s with value %s", _class.__name__, member)
                            con.execute(sa.text("ALTER TYPE {} ADD VALUE '{}'".format(_class.__name__.lower(), member)))
                            con.commit()


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
            from .logger import log

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

    def extend_enums(self, module):
        return extend_enums(self.session(), self.engine, module)


class AsyncSQL(SQL):
    """Asynchronous SQLAlchemy client. Creates async engine and async sessionmaker"""

    def _create_engine(self, url: str, echo: bool = True, **kwargs):
        """Creates asynchronous engine"""
        self._engine = create_async_engine(url, echo=echo, **kwargs)

    def _create_sessionmaker(self):
        """Creates asynchronous session factory"""
        self._session = async_sessionmaker(bind=self._engine)

    async def create_tables(self, base: Base = Base):
        """Creates tables asynchronously. To be used with await"""
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def drop_tables(self, base: Base = Base):
        """Drops tables asynchronously. To be used with await"""
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)
