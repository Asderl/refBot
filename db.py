import aiosqlite as asql
from os import path
import asyncio

db_path = path.join(path.dirname(__file__), "database", "referals")

async def add_new_user(table_name: str, user_id: str):
    values = [i[0] for i in await get_all_users("main")]
    if user_id in values:
        print("id already presented!")
        return
    else:
        db = await asql.connect(db_path)
        await db.execute(f"INSERT INTO {table_name}(user_id) VALUES({user_id})")
        await db.commit()
        await db.close()

async def get_all_users(table_name: str):
    db = await asql.connect(db_path)
    cursor = await db.execute(f"SELECT * FROM {table_name}")
    values = await cursor.fetchall()
    await db.close()
    return values
