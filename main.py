import asyncio
import logging

from src.api_handler import get_info
from src.bot_handler import BotHandler
from src.scheduler import PostScheduler

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Приложение запущено")
    while True:
        logger.info("Цикл запущен")
        all_info, last_row = get_info()
        if all_info:
            logger.info("Проверка прошла успешно, бот начинает работу")
            bot = BotHandler(all_info)
            await bot.sort_as_is()
            await bot.sort_projects()
            await bot.sort_vacancies()
            scheduler = PostScheduler(all_info, last_row, bot)
            await scheduler.run()
        else:
            logger.info("Проверка не прошла, бот идет спать на 2 часа")
            await asyncio.sleep(7200)
            continue

if __name__ == "__main__":
    asyncio.run(main())