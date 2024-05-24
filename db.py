from typing import Iterable
import aiosqlite as asql
from log import Logger
from os import path

class Database:
    def __init__(self, *table_path: str) -> None:
        db_path = path.dirname(__file__)
        for file in table_path:
            db_path = path.join(db_path, file)
        self.db_path = db_path
        self.logger = Logger("db")

    async def add_new_user(self, table_name: str, user_id: str) -> None:
        values: list[str] = [i[0] for i in await self.get_all_users("main")]
        if user_id in values:
            self.logger.info("id already presented!")
            return
        else:
            db = await asql.connect(self.db_path)
            await db.execute(f"INSERT INTO {table_name}(user_id, referals) VALUES({user_id}, 0)")
            await db.commit()
            await db.close()

    async def get_all_users(self, table_name: str) -> Iterable[asql.Row]:
        db = await asql.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM {table_name}")
        values = await cursor.fetchall()
        await db.close()
        return values
