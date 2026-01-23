import os
import logging

from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("token")
chat_id = os.getenv("chat_id")
bot = Bot(token=TOKEN)

# topics_test = {"Projects": 4, "As is": 3, "Vacancies": 5}

topics = {"Projects": 2, "As is": 19, "Vacancies": 4}

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BotHandler:
    def __init__(self, all_info):
        self.rows = all_info
        self.as_is = None
        self.projects = None
        self.vacancies = None

    async def append_new_info(self, new_data):
        """обновляет данные"""
        self.rows.update(new_data)
        logger.info("Добавляю новые данные в бота")
        await self.sort_as_is()
        await self.sort_projects()
        await self.sort_vacancies()

    async def sort_as_is(self):
        logger.info("Сортирую данные в as is")
        row_dict = self.rows
        as_is_dict = {}
        for row, values in row_dict.items():
            if not values:
                as_is_dict[row] = []
            else:
                if values[0] == "As is":
                    as_is_dict[row] = values
        self.as_is = as_is_dict

    async def sort_vacancies(self):
        logger.info("Сортирую вакансии")
        row_dict = self.rows
        vacancies = {}
        for row, values in row_dict.items():
            if not values:
                vacancies[row] = []
            else:
                if values[0] == "Vacancies":
                    vacancies[row] = values
        self.vacancies = vacancies

    async def sort_projects(self):
        logger.info("Сортирую проекты")
        row_dict = self.rows
        projects = {}
        for row, values in row_dict.items():
            if not values:
                projects[row] = []
            else:
                if values[0] == "Projects":
                    projects[row] = values
        self.projects = projects

    async def send_projects(self) -> None:
        """постит данные"""
        logger.info("Начинаю постить в проекты")
        for row, values in self.projects.items():
            safe_values = []
            for i in range(5):
                if values and len(values) > i and values[i] is not None:
                    safe_values.append(values[i])
                else:
                    safe_values.append("")

            chanel = safe_values[0]
            tegs = safe_values[1].replace(",", " ")
            description = safe_values[2]
            link = safe_values[3][0] if type(safe_values[3]) == list and  len(safe_values[3]) == 2  else safe_values[3]
            link_text = safe_values[3][1] if type(safe_values[3]) == list and  len(safe_values[3]) == 2 else ''
            header = safe_values[4]
            message_thread_id = topics.get(chanel)
            if link:

                if link[0] == "@":
                    text = f"""{tegs}
<b>{header}</b>
{description}
                
Канал: {link}
"""
                elif not (link.endswith(".ru") or link.endswith(".com")):
                    text = f"""{tegs}
<b>{header}</b>
{description}

Ссылка: <a href='{link}'> {link_text}</a>
"""
                else:
                    text = f"""{tegs}
<b>{header}</b>
{description}

Напиши по почте: {link}
"""
            else:
                text = f"""{tegs}
<b>{header}</b>
{description}

Без ссылки
"""
            await bot.send_message(
                chat_id, text, parse_mode="HTML", message_thread_id=message_thread_id
            )
            del self.projects[row]
            logger.info("Удалил данные заканчиваю постить")
            break


    async def send_as_is(self) -> None:
        logger.info("Начинаю постить в as is ")
        for row, values in self.as_is.items():

            safe_values = []
            for i in range(5):
                if values and len(values) > i and values[i] is not None:
                    safe_values.append(values[i])
                else:
                    safe_values.append("")

            chanel = safe_values[0]
            tegs = safe_values[1].replace(",", " ")
            description = safe_values[2]
            link = safe_values[3][0] if type(safe_values[3]) == list and len(safe_values[3]) == 2 else safe_values[3]
            link_text = safe_values[3][1] if type(safe_values[3]) == list and len(safe_values[3]) == 2 else ''
            header = safe_values[4]
            message_thread_id = topics.get(chanel)
            if link:

                if link[0] == "@":
                    text = f"""{tegs}
<b>{header}</b>
{description}

Канал: {link}
"""
                elif not (link.endswith(".ru") or link.endswith(".com")):
                    text = f"""{tegs}
<b>{header}</b>
{description}

Ссылка: <a href='{link}'> {link_text}</a>
"""
                else:
                    text = f"""{tegs}
<b>{header}</b>
{description}

Напиши по почте: {link}
"""
            else:
                text = f"""{tegs}
<b>{header}</b>
{description}

Без ссылки
"""
            await bot.send_message(
                chat_id, text, parse_mode="HTML", message_thread_id=message_thread_id
            )
            del self.as_is[row]
            logger.info("Удалил данные, заканчиваю постить")
            break

    async def send_vacancies(self) -> None:
        """постит данные"""
        logger.info("Начинаю постить в вакансии")
        for row, values in self.vacancies.items():
            safe_values = []
            for i in range(5):
                if values and len(values) > i and values[i] is not None:
                    safe_values.append(values[i])
                else:
                    safe_values.append("")

            chanel = safe_values[0]
            tegs = safe_values[1].replace(",", " ")
            description = safe_values[2]
            link = safe_values[3][0] if type(safe_values[3]) == list and len(safe_values[3]) == 2 else safe_values[3]
            link_text = safe_values[3][1] if type(safe_values[3]) == list and len(safe_values[3]) == 2 else ''
            header = safe_values[4]
            message_thread_id = topics.get(chanel)
            if link:

                if link[0] == "@":
                    text = f"""{tegs}
<b>{header}</b>
{description}

Канал: {link}
"""
                elif not (link.endswith(".ru") or link.endswith(".com")):
                    text = f"""{tegs}
<b>{header}</b>
{description}

Ссылка: <a href='{link}'> {link_text}</a>
"""
                else:
                    text = f"""{tegs}
<b>{header}</b>
{description}

Напиши по почте: {link}
"""
            else:
                text = f"""{tegs}
<b>{header}</b>
{description}

Без ссылки
"""
            await bot.send_message(
                chat_id, text, parse_mode="HTML", message_thread_id=message_thread_id
            )
            del self.vacancies[row]
            logger.info("Удалил данные заканчиваю постить")
            break

