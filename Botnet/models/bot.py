from typing import Any
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base: Any = declarative_base()


class Bot(Base):
    __tablename__: str = 'infecteds'

    id = Column(Integer, primary_key=True)
    host: str = Column('host', String(100))
    username: str = Column('username', String(100))
    password: str = Column('password', String(100))
    port: str = Column('port', Integer)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"


if __name__ == '__main__':
    engine = create_engine('sqlite:///victims.db')
    Base.metadata.create_all(engine)

