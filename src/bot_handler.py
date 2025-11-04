import os

from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("token")
chat_id = os.getenv("chat_id")
bot = Bot(token=TOKEN)

# topics_test = {"Projects": 4, "As is": 3, "Vacancies": 5}

topics = {"Projects": 2, "As is": 19, "Vacancies": 4}


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
            for i in range(4):
                if values and len(values) > i and values[i] is not None:
                    safe_values.append(values[i])
                else:
                    safe_values.append("")

            chanel = safe_values[0]
            tegs = safe_values[1].replace(",", " ")
            description = safe_values[2]
            link = safe_values[3][0] if type(safe_values[3]) == list else safe_values[3]
            link_text = safe_values[3][1] if type(safe_values[3]) == list else ''
            message_thread_id = topics.get(chanel)
            #сделать заголвки для столбца с заголовками, залить на сервак и показать булату

            if link[0] == "@":
                text = f"""{tegs}
{description}
                
Канал: {link}
"""
            else:
                text = f"""{tegs}
{description}

Ссылка: <a href='{link}'> {link_text}</a>
"""
            await bot.send_message(
                chat_id, text, parse_mode="HTML", message_thread_id=message_thread_id
            )
            del self.rows[row]
            break
