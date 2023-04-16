from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass, Field
from contextlib import contextmanager


@dataclass
class Connections:
    path: str = r"../models/victims.db"

    @contextmanager
    def connection(self) -> 'Session':
        engine = create_engine(f"sqlite:///{self.path}")
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
