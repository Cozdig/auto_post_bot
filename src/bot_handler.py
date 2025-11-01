import os

from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("token")
chat_id = os.getenv("chat_id")
bot = Bot(token=TOKEN)

topics = {"projects": 4, "as_is": 3, "vacancies": 5}

topics_job = {"projects": 2, "as_is": 19, "vacancies": 4}

projects = ["Хакатон", "Проект", "Стажировки", "Олимпиады"]

as_is = ["Обучение", "Полезно знать", "Экскурсии"]

vacancies = ["Офферы"]

class BotHandler:
    def __init__(self, all_info):
        self.rows = all_info

    async def append_new_info(self, new_data):
        """обновляет данные"""
        self.rows.update(new_data)

    async def send_message(self) -> None:
        """постит данные"""
        for row, values in self.rows.items():

            safe_values = []
            for i in range(6):
                if values and len(values) > i and values[i] is not None:
                    safe_values.append(str(values[i]))
                else:
                    safe_values.append("")

            title = safe_values[0]
            link = safe_values[1]
            category = safe_values[2]
            type_ = safe_values[3]
            ddl = safe_values[4] or "-"
            description = safe_values[5] or "-"

            if category in projects:
                message_thread_id = topics.get("projects")
            elif category in as_is:
                message_thread_id = topics.get("as_is")
            elif category in vacancies:
                message_thread_id = topics.get("vacancies")
            else:
                message_thread_id = 1
            if link == "@":
                text = f"""<b>{title.replace(".", "․")}</b>
                
<b>DDL: {ddl}</b>
раздел: {category}
тип: {type_}

{description}
Канал {link}
"""
            else:
                text = f"""<b>{title.replace(".", "․")}</b>
                
<b>DDL: {ddl}</b>
раздел: {category}
тип: {type_}

{description}
<a href='{link}'>Тык</a>
"""
            await bot.send_message(
                chat_id, text, parse_mode="HTML", message_thread_id=message_thread_id
            )
            del self.rows[row]
            break
