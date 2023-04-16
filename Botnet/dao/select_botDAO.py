from typing import Any
from connections import Connections
from dataclasses import dataclass
from models import Bot


@dataclass
class SelectBotDao:

    conn: Connections = Connections()

    def select(self) -> Any:
        with self.conn.connection() as bots:
            for bot in bots.query(Bot):
                print(bot.username)


if __name__ == '__main__':
    s = SelectBotDao()
    s.select()
