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

    async def add_new_user(self, table_name: str, user_id: str, parent: str = 0) -> None|int:
        values: list[str] = [i[0] for i in await self.get_all_users("main")]
        if user_id in values:
            self.logger.info(f"user {user_id} already presented!")
            return -1
        else:
            db = await asql.connect(self.db_path)
            await db.execute(f"INSERT INTO {table_name}(user_id, referals, parent) VALUES({user_id}, 0, {parent})")
            await db.commit()
            await db.close()

    async def get_all_users(self, table_name: str) -> Iterable[asql.Row]:
        db = await asql.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM {table_name}")
        values = await cursor.fetchall()
        await db.close()
        return values

    async def get_parent(self, table_name: str, user_id: str) -> str|None:
        values: list[str] = [i[0] for i in await self.get_all_users("main")]
        if user_id in values:
            db = await asql.connect(self.db_path)
            cursor = await db.execute(f"SELECT parent FROM {table_name} WHERE user_id = {user_id}")
            parent = await cursor.fetchone()
            await db.close()
            self.logger.debug(parent[0])
            return parent[0]

    async def add_referal(self, table_name: str, parent: str) -> None:
        db = await asql.connect(self.db_path)
        await db.execute(f"UPDATE {table_name} SET referals = referals + 1 WHERE user_id = {parent}")
        await db.commit()
        await db.close()
