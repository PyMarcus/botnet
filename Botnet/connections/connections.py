from typing import Any
from pexpect import pxssh
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass, Field
from contextlib import contextmanager


@dataclass
class Connections:
    path: str = r"../models/victims.db"

    @contextmanager
    def connection_database(self) -> 'Session':
        engine = create_engine(f"sqlite:///{self.path}")
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session

    @contextmanager
    def connection_ssh(self, host, user, password) -> Any:
        try:
            session: Any = pxssh.pxssh()
            session.login(host, user, password)
        except pxssh.ExceptionPxssh as e:
            print(f"Failed to connect to {host} - {user}")
        else:
            yield session
