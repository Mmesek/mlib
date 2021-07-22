from sqlalchemy import Column, TIMESTAMP, Integer, String, func
from sqlalchemy.orm import declarative_base, declared_attr, Query
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
import datetime

from typing import List, TypeVar, Type
T = TypeVar('T', bound='Base')

class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__  #.lower()
    @classmethod
    def filter(cls: Type[T], session: Session, **kwargs) -> Query:
        ''':param kwargs: Column = Value'''
        return session.query(cls).filter_by(**kwargs)
    @classmethod
    def fetch_or_add(cls: Type[T], s: Session, **kwargs) -> T:
        m = cls.filter(s, **kwargs).first()
        if not m:
            m = cls(**kwargs)
            s.add(m)
        return m
    @classmethod
    def fetch_or_add_multiple(cls: Type[T], s: Session, *ids: int) -> List[T]:
        objects = []
        for id in ids:
            objects.append(cls.fetch_or_add(s, id=id))
        return objects
    @classmethod
    def by_id(cls: Type[T], s: Session, id: int) -> T:
        return cls.filter(s, id = id).first()
    @classmethod
    def by_name(cls: Type[T], s: Session, name: str) -> T:
        return cls.filter(s, name = name).first()
#    def __repr__(self) -> str:
#        return "{}({})".format(
#            self.__class__.__name__,
#            ", ".join(["{}={!r}".format(attr, getattr(self, attr)) for attr in vars(self) if not attr.startswith('_')])
#        )
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

Base = declarative_base(cls=Base)
#Meta = MetaData()

class ID:
    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

class Default(ID):
    name: str = Column(String, unique=True, nullable=False)
    def __init__(self, name) -> None:
        self.name = name

class File(ID):
    filename: str = Column(String)

class Timestamp:
    timestamp: datetime.datetime = Column(TIMESTAMP(timezone=True), server_default=func.now())

class TimestampUpdate:
    timestamp: datetime.datetime = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


def extend_enums(session: Session, engine: Engine, module):
    '''Extends existing DB Enum with new values from Coded Enum'''
    import enum
    from inspect import isclass
    from sqlalchemy import text
    with session.begin() as s:
        for _class in vars(module).values():
            if isclass(_class) and issubclass(_class, enum.Enum) and len(_class.__members__) > 0:
                try:
                    r = s.query(text('unnest(enum_range(NULL::{}))'.format(_class.__name__.lower()))).all()
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
                            con.execute(text("ALTER TYPE {} ADD VALUE '{}'".format(_class.__name__.lower(), member)))
                            con.commit()

class SQL:
    __slots__ = ('engine', 'session')
    engine: Engine
    session: Session
    def __init__(self, db='postgresql', user='postgres', password='postgres', location='192.168.1.5', port=5432, name='beta', echo=True):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        try:
            self.engine = create_engine(f'{db}://{user}:{password}@{location}:{port}/{name}', client_encoding='utf8', echo=echo, future=True)
        except Exception as ex:
            from .logger import log
            log.exception("Connecting to Remote DB failed! Falling back to local SQLite", exc_info=ex)
            self.engine = create_engine(f"sqlite:///{name}.db", echo=echo, future=True)
        self.session = sessionmaker(bind=self.engine, future=True)
    @property
    def Session(self):
        return self.session
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
    def merge(self, mapping):
        with self.session.begin() as s:
            s.merge(mapping)
    def add(self, mapping):
        with self.session.begin() as s:
            s.add(mapping)
    def delete(self, mapping):
        with self.session.begin() as s:
            s.delete(mapping)
    def merge_or_add(self, queried_result, mapping):
        if queried_result:
            return self.merge(mapping)
        return self.add(mapping)
    def extend_enums(self, module):
        return extend_enums(self.session, self.engine, module)