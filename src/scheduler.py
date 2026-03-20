import asyncio
import logging
import gc

from datetime import datetime
from src.api_handler import get_info

schedule = [1, 2, 3, 4] # Простой список дней: вторник-пятница

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PostScheduler:
    def __init__(self, all_info, bot):

        self.all_info = all_info
        self.last_hour_sent = None
        self.ob_bot = bot
        self.last_check = 0

    async def memory_cleanup(self):
        """Периодическая очистка памяти"""
        collected = gc.collect()
        logger.info(f"Очищено {collected} объектов памяти")


    async def check_new_posts(self):
        """Проверяет новые посты в таблице в понедельник"""
        logger.info("Проверяю новые посты в понедельник")
        all_info = get_info()
        self.last_check = 1
        logger.info(f"Добавляю данные")
        self.all_info = all_info
        await self.ob_bot.append_new_info(all_info)
        logger.info("Новые посты добавлены")
        return True

    async def do_as_is_posts(self):
        logger.info("Проверяю данные в as is")
        now = datetime.now()
        current_day = now.weekday()
        current_hour = now.hour
        # Проверяем день недели (понедельник)
        if current_day == 0:
            # Проверяем время (10-11)
            if 7 <= current_hour < 8:
                if self.last_hour_sent != current_hour:
                    logger.info("Запускаю бота на пост в as is")
                    await self.ob_bot.send_as_is()
                    self.last_hour_sent = current_hour
                    return True
                else:
                    logger.info("Сейчас не 10-11 часов для поста")
                    return False
        return False

    async def do_other_posts(self):
        """Отправляет посты если сейчас подходящее время"""
        logger.info("Проверяю данные в проекты и вакансии")
        now = datetime.now()
        current_day = now.weekday()
        current_hour = now.hour
        # Проверяем день недели (вторник-пятница)
        if current_day in schedule:
            # Проверяем время (10-11 или 12-13 часов)
            if 7 <= current_hour < 8:
                if self.last_hour_sent != current_hour:
                    logger.info("Запускаю бота на пост в projects")
                    await self.ob_bot.send_projects()
                    self.last_hour_sent = current_hour
                    return True
                else:
                    logger.info("сейчас не 10-11 часов, пост уже был")
                    return False
            elif 9 <= current_hour < 10:
                if self.last_hour_sent != current_hour:
                    logger.info("Запускаю бота на пост в vacancies")
                    await self.ob_bot.send_vacancies()
                    self.last_hour_sent = current_hour
                    return True
                else:
                    logger.info("сейчас не 12-13 часов, пост уже был")
                    return False
        return False

    async def check_day(self):
        """Основная функция проверки дня и времени"""
        now = datetime.now()
        current_day = now.weekday()

        if now.hour == 15 or now.hour == 3:
            await self.memory_cleanup()

        if current_day != 0:
            logger.info("Сегодня не понедельник, меняю переменную")
            self.last_check = 0

        if current_day == 0 and self.last_check == 0:  # Понедельник
            logger.info("Сегодня понедельник, запускаю расписание понедельника")
            await self.run_mon_schedule()

        if current_day in schedule:  # Вт-Пт
            logger.info("Сегодня вторник, запускаю расписание вторника")
            await self.run_daily_schedule()

        elif current_day != 0:
            logger.info("Сегодня выходные, иду спать")
            await self.wait_until_monday()

    async def run_mon_schedule(self):
        """Запускает расписание понедельника"""
        await self.check_new_posts()

        while True:
            now = datetime.now()
            current_hour = now.hour

            if current_hour >= 10:
                logger.info("Сейчас больше 13 часов")
                self.last_hour_sent = None
                break
            logger.info("Запускаю бота")
            await self.do_as_is_posts()

            current_minute = now.minute
            minutes_to_wait = 30 - (current_minute % 30)
            wait_seconds = minutes_to_wait * 60
            logger.info(f"Иду спать на {wait_seconds} секунд")
            await asyncio.sleep(wait_seconds)

    async def run_daily_schedule(self):
        """Запускает ежедневное расписание"""
        while True:
            now = datetime.now()
            current_hour = now.hour

            if current_hour >= 10:
                logger.info("Сейчас больше 13 часов")
                self.last_hour_sent = None
                break

            logger.info("Запускаю бота")
            await self.do_other_posts()

            current_minute = now.minute
            minutes_to_wait = 30 - (current_minute % 30)
            wait_seconds = minutes_to_wait * 60
            logger.info(f"Иду спать на {wait_seconds} секунд")
            await asyncio.sleep(wait_seconds)

    async def wait_until_monday(self):
        """Ждем следующего понедельника"""
        now = datetime.now()
        now_hour = now.hour
        days_until_monday = 7 - now.weekday()

        wait_seconds = (days_until_monday * 24 * 3600) - (now_hour * 3600)
        logger.info(f"Иду спать на {wait_seconds} секунд до понедельника")
        await asyncio.sleep(wait_seconds)

    async def run(self):
        """Основной цикл программы"""
        while True:
            logger.info(f"Запускаю scheduler")
            now = datetime.now()
            current_hour = now.hour
            if 6 <= current_hour < 10:
                logger.info(f"Сейчас корректное время, иду проверять день")
                await self.check_day()

            else:
                logger.info(f"Сейчас не корректное время, иду спать на час")
                await asyncio.sleep(3600) #спит час




