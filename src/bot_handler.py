import os
import asyncio

from aiogram import Bot
from dotenv import load_dotenv

from src.api_handler import get_hyperlinks

load_dotenv()
TOKEN = os.getenv('token')
chat_id = os.getenv('chat_id')
bot = Bot(token=TOKEN)



async def send_message() -> None:
    posts = get_hyperlinks()
    for row, link in posts.items():
        if link[0] == "@":
            await bot.send_message(chat_id, f"Строка {row}, Тг-канал: {link}")
        else:
            await bot.send_message(chat_id, f"Строка {row}, <a href='{link}'>Тык</a>", parse_mode="HTML")
        await asyncio.sleep(3)



async def create_auto_post():
    task = asyncio.create_task(send_message())
    await task
