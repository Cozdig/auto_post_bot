import asyncio
from datetime import datetime
from src.api_handler import get_info

schedule = [1, 2, 3, 4]  # Простой список дней: вторник-пятница


class PostScheduler:
    def __init__(self, all_info, last_row, bot):
        self.all_info = all_info
        self.last_row = last_row
        self.last_hour_sent = None
        self.ob_bot = bot

    async def check_new_posts(self):
        """Проверяет новые посты в таблице"""
        new_all_info, new_last_row = get_info()
        if new_last_row != self.last_row:
            only_new_data = {}
            for row_num, row_data in new_all_info.items():
                if row_num > self.last_row:
                    only_new_data[row_num] = row_data

            # Полностью заменяем старые данные на новые
            self.all_info = only_new_data
            self.ob_bot.append_new_info(only_new_data)
            self.last_row = new_last_row
            return True
        return False

    async def do_posts(self):
        """Отправляет посты если сейчас подходящее время"""
        now = datetime.now()
        current_day = now.weekday()
        current_hour = now.hour

        # Проверяем день недели (вторник-пятница)
        if current_day in schedule:
            # Проверяем время (10-11 или 12-13 часов)
            if 10 <= current_hour < 11 or 12 <= current_hour < 13:
                if self.last_hour_sent != current_hour:
                    await self.ob_bot.send_message()
                    self.last_hour_sent = current_hour
                    return True
                else:
                    return False
        return False

    async def check_day(self):
        """Основная функция проверки дня и времени"""
        now = datetime.now()
        current_day = now.weekday()

        if current_day == 1:  # Вторник
            await self.check_new_posts()

        if current_day in schedule:  # Вт-Пт
            await self.run_daily_schedule()

        else:
            await self.wait_until_tuesday()

    async def run_daily_schedule(self):
        """Запускает ежедневное расписание"""

        while True:
            now = datetime.now()
            current_day = now.weekday()
            current_hour = now.hour

            if current_hour >= 13:
                self.last_hour_sent = None
                break

            await self.do_posts()

            current_minute = now.minute
            minutes_to_wait = 30 - (current_minute % 30)
            if minutes_to_wait == 30:
                minutes_to_wait = 0

            wait_seconds = minutes_to_wait * 60
            await asyncio.sleep(wait_seconds)

    async def wait_until_tuesday(self):
        """Ждем следующего вторника"""
        now = datetime.now()
        days_until_tuesday = (1 - now.weekday()) % 7
        if days_until_tuesday == 0:
            days_until_tuesday = 7

        wait_seconds = days_until_tuesday * 24 * 3600
        await asyncio.sleep(wait_seconds)

    async def run(self):
        """Основной цикл программы"""
        while True:
            await self.check_day()



