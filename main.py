import asyncio

from src.api_handler import get_info
from src.bot_handler import BotHandler
from src.scheduler import PostScheduler


async def main():
    all_info, last_row = get_info()
    bot = BotHandler(all_info)
    test_scheduler = PostScheduler(all_info, last_row, bot)
    await test_scheduler.run()

if __name__ == "__main__":
    asyncio.run(main())