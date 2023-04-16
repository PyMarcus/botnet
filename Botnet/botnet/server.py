from connections import Connections
from dao import SelectBotDao
from dataclasses import dataclass


@dataclass
class BotnetServer:

    __conn: Connections = Connections()
    __bots: SelectBotDao = SelectBotDao()

    def get_all_bots(self) -> object:
        for bot in self.__bots.select():
            yield bot

    def get_bot(self, **kwargs) -> object:
        return self.__bots.select_one(**kwargs)


if __name__ == '__main__':
    bs: BotnetServer = BotnetServer()
    for bot in bs.get_all_bots():
        print(bot)
    print(bs.get_bot(id=1))
    print(bs.get_bot(user='marcus'))

