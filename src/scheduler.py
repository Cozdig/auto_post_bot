import asyncio
from datetime import datetime
from src.api_handler import get_info

schedule = [1, 2, 3, 4] # Простой список дней: вторник-пятница


class PostScheduler:
    def __init__(self, all_info, last_row, bot):

        self.all_info = all_info
        self.last_row = last_row
        self.last_hour_sent = None
        self.ob_bot = bot
        self.last_check = 0

    async def check_new_posts(self):
        """Проверяет новые посты в таблице в понедельник"""
        new_all_info, new_last_row = get_info()
        self.last_check = 1
        if new_last_row != self.last_row:
            only_new_data = {}
            for row_num, row_data in new_all_info.items():
                if row_num > self.last_row:
                    only_new_data[row_num] = row_data
            # Полностью заменяем старые данные на новые
            self.all_info = only_new_data
            await self.ob_bot.append_new_info(only_new_data)
            self.last_row = new_last_row
            return True
        return False

    async def do_ai_is_posts(self):
        now = datetime.now()
        current_day = now.weekday()
        current_hour = now.hour
        # Проверяем день недели (понедельник)
        if current_day == 0:
            # Проверяем время (10-11)
            if 10 <= current_hour < 11:
                if self.last_hour_sent != current_hour:
                    await self.ob_bot.send_as_is()
                    self.last_hour_sent = current_hour
                    return True
                else:
                    return False
        return False

    async def do_other_posts(self):
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

        if current_day != 0:
            self.last_check = 0

        if current_day == 0 and self.last_check == 0:  # Понедельник
            await self.run_mon_schedule()

        if current_day in schedule:  # Вт-Пт
            await self.run_daily_schedule()

        else:
            await self.wait_until_monday()

    async def run_mon_schedule(self):
        """Запускает расписание понедельника"""
        await self.check_new_posts()

        while True:
            now = datetime.now()
            current_hour = now.hour

            if current_hour >= 13:
                self.last_hour_sent = None
                break

            await self.do_ai_is_posts()

            current_minute = now.minute
            minutes_to_wait = 30 - (current_minute % 30)
            wait_seconds = minutes_to_wait * 60
            await asyncio.sleep(wait_seconds)

    async def run_daily_schedule(self):
        """Запускает ежедневное расписание"""
        while True:
            now = datetime.now()
            current_hour = now.hour

            if current_hour >= 13:
                self.last_hour_sent = None
                break

            await self.do_other_posts()

            current_minute = now.minute
            minutes_to_wait = 30 - (current_minute % 30)
            wait_seconds = minutes_to_wait * 60
            await asyncio.sleep(wait_seconds)

    async def wait_until_monday(self):
        """Ждем следующего понедельника"""
        now = datetime.now()
        days_until_tuesday = (0 - now.weekday()) % 7
        if days_until_tuesday == 0:
            days_until_tuesday = 7

        wait_seconds = days_until_tuesday * 24 * 3600
        await asyncio.sleep(wait_seconds)

    async def run(self):
        """Основной цикл программы"""
        while True:
            now = datetime.now()
            current_hour = now.hour
            if 9 <= current_hour < 13:
                await self.check_day()

            else:
                await asyncio.sleep(3600) #спит час




