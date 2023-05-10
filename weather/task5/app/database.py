import threading

from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .config import get_config


class Database:
    class __Database:
        __config = get_config()

        def __init__(self) -> None:
            self.engine = create_engine(
                url = URL.create(
                    "postgresql",
                    username= self.__config['POSTGRES_USER'],
                    password= self.__config['POSTGRES_PASSWORD'],
                    host= self.__config['POSTGRES_HOSTNAME'],
                    port = self.__config['DATABASE_PORT'],
                    database= self.__config['POSTGRES_DB'],
    )
            )       
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Base = declarative_base()


        def session(self) -> Session:
            db_session = self.SessionLocal()
            try:
                yield db_session
            finally:
                db_session.close()

    _db = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._db is None:
            with cls._lock:
                if not cls._db:
                    cls._db = cls.__Database()
        return cls._db