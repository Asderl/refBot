from typing import Iterable
import aiosqlite as asql
from log import Logger
from os import path

class Database:
    """Class Database provides asynchronous access to sqlite database

    Params: relative path to database file, each directory in separate string
    """
    def __init__(self, *table_path: str) -> None:
        db_path = path.dirname(__file__)
        for file in table_path:
            db_path = path.join(db_path, file)
        self.db_path = db_path
        self.logger = Logger("db")

    #Add new user to specified table of database, user don't have parent by default
    async def add_new_user(self, table_name: str, user_id: str, parent: str = "0") -> None|int:
        if await self.get_user(table_name, user_id) == user_id:
            self.logger.info(f"user {user_id} already presented!")
            return -1
        else:
            db = await asql.connect(self.db_path)
            await db.execute(f"INSERT INTO {table_name}(user_id, referals, parent) VALUES({user_id}, 0, {parent})")
            await db.commit()
            await db.close()

    #Get user from specified table of database
    async def get_user(self, table_name: str, user_id: str) -> str|None:
        db = await asql.connect(self.db_path)
        cursor = await db.execute(f"SELECT user_id FROM {table_name} WHERE user_id={user_id}")
        value = await cursor.fetchone()
        await db.close()
        if value != None:
            return value[0]
        return None

    #Get all users from specified table of database
    async def get_all_users(self, table_name: str) -> Iterable[asql.Row]:
        db = await asql.connect(self.db_path)
        cursor = await db.execute(f"SELECT * FROM {table_name}")
        values = await cursor.fetchall()
        await db.close()
        return values

    #Get user parent
    async def get_parent(self, table_name: str, user_id: str) -> str|None:
        if await self.get_user(table_name, user_id) == user_id:
            db = await asql.connect(self.db_path)
            cursor = await db.execute(f"SELECT parent FROM {table_name} WHERE user_id = {user_id}")
            parent = await cursor.fetchone()
            await db.close()
            self.logger.debug(parent[0])
            return parent[0]

    #Increase user referral count
    async def add_referal(self, table_name: str, parent: str) -> None:
        db = await asql.connect(self.db_path)
        await db.execute(f"UPDATE {table_name} SET referals = referals + 1 WHERE user_id = {parent}")
        await db.commit()
        await db.close()

    #Get user referral count
    async def get_ref_count(self, table_name: str, user_id: str) -> int:
        db = await asql.connect(self.db_path)
        cursor = await db.execute(f"SELECT referals FROM {table_name} WHERE user_id = {user_id}")
        ref_count = await cursor.fetchone()
        await db.close()
        return ref_count[0]

    #Get user wallet
    async def get_wallet(self, table_name: str, user_id: str) -> str:
        db = await asql.connect(self.db_path)
        cursor = await db.execute(f"SELECT wallet FROM {table_name} WHERE user_id={user_id}")
        wallet = await cursor.fetchone()
        await db.close()
        return wallet[0]

    #Add new wallet
    async def add_wallet(self, table_name: str, user_id: str, wallet: str) -> None:
        db = await asql.connect(self.db_path)
        await db.execute(f"UPDATE {table_name} SET wallet='{wallet}' WHERE user_id={user_id}")
        await db.commit()
        await db.close()
