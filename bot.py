from aiogram import Bot, Dispatcher, Router
from db import *


if __name__ == "__main__":
    asyncio.run(add_new_user("main", "1234567890"))
