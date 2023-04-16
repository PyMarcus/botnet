from typing import Any
from connections import Connections
from dataclasses import dataclass
from models import Bot


@dataclass
class SelectBotDao:

    conn: Connections = Connections()

    def select(self) -> Any:
        with self.conn.connection_database() as bots:
            for bot in bots.query(Bot):
                yield bot

    def select_one(self, **kwargs) -> Any:
        with self.conn.connection_database() as bots:
            if kwargs.get('id'):
                for bot in bots.query(Bot).\
                        filter(Bot.id == kwargs.get('id')):
                    return bot
            elif kwargs.get('user'):
                for bot in bots.query(Bot).\
                        filter(Bot.username == kwargs.get('user')):
                    return bot


if __name__ == '__main__':
    s = SelectBotDao()
    s.select()
