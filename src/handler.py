import os
import asyncio


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('token')

dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: Message) -> None:
    await message.reply("Привет! Я ваш первый Telegram-бот.")

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())