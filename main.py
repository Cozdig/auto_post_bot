import asyncio

from src.api_handler import get_info
from src.bot_handler import BotHandler
from src.scheduler import PostScheduler


async def main():

    while True:
        all_info, last_row = get_info()
        if all_info:
            bot = BotHandler(all_info)
            scheduler = PostScheduler(all_info, last_row, bot)
            await scheduler.run()
        else:
            await asyncio.sleep(7200)
            continue

if __name__ == "__main__":
    asyncio.run(main())