from aiogram.utils.deep_linking import decode_payload, create_start_link
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, User
from aiogram.enums import ParseMode
from bot_token import TOKEN
from db import Database
import asyncio

router = Router()
dp = Dispatcher()

table_name = "main"
db = Database("database", "referals")
bot = Bot(TOKEN)

@router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def command_start(message: Message, command: CommandObject) -> None:
    args = command.args
    if args != None:
        db.add_new_user("main", str(message.from_user.id))
    else:
        payload = decode_payload(args)
        await db.add_new_user("main", str(message.from_user.id))

@router.message(Command("ref"))
async def command_referal(message: Message) -> None:
    ref_link = await gen_ref(message.from_user.id)
    message.answer(f"Your referal link: {ref_link}")

async def gen_ref(user_id: str) -> str:
    return await create_start_link(bot, user_id, encode=True)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
