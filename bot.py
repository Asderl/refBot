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

@router.message(CommandStart(deep_link=True))
async def command_start_dl(message: Message, command: CommandObject) -> None:
    args = command.args
    payload = decode_payload(args)
    await db.add_new_user("main", str(message.from_user.id), payload)
    await db.add_referal("main", payload)

@router.message(Command("start"))
async def command_start(message: Message) -> None:
    await db.add_new_user("main", str(message.from_user.id))

@router.message(Command("ref"))
async def command_referal(message: Message) -> None:
    ref_link = await create_start_link(bot, message.from_user.id, encode=True)
    await message.answer(f"Your referal link: {ref_link}")


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
