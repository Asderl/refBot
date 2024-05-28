from aiogram.utils.deep_linking import decode_payload, create_start_link
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from bot_token import TOKEN
from db import Database
import asyncio

router = Router()
dp = Dispatcher()

table_name = "main" #Name of table in database
db = Database("database", "referals") #Database path is ./database/referals
bot = Bot(TOKEN) #Telegram bot token

#Handler for /start command with payload
@router.message(CommandStart(deep_link=True))
async def command_start_dl(message: Message, command: CommandObject) -> None:
    args = command.args
    payload = decode_payload(args)
    #Check is user id different than in referral link
    if payload == str(message.from_user.id):
        await message.answer("You can't be referral of yourself")
        await db.add_new_user(table_name, str(message.from_user.id))
        return
    #Check is user not already presented in table
    if await db.add_new_user(table_name, str(message.from_user.id), payload) != -1:
        await db.add_referal(table_name, payload)

#Handler for /start command without payload
@router.message(Command("start"))
async def command_start(message: Message) -> None:
    await db.add_new_user(table_name, str(message.from_user.id))

#Handler for /ref command - show referral count and referral link
@router.message(Command("ref"))
async def command_referal(message: Message) -> None:
    ref_link = await create_start_link(bot, message.from_user.id, encode=True)
    ref_count = await db.get_ref_count(table_name, str(message.from_user.id))
    await message.answer(f"Your referrals: {ref_count}\nYour referral link: {ref_link}")

#Main function - start bot polling
async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

#Entry point
if __name__ == "__main__":
    asyncio.run(main())
