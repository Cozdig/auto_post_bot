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
        self.as_is = None

    async def append_new_info(self, new_data):
        """обновляет данные"""
        self.rows.update(new_data)
        await self.sort_as_is()
        await self.sort_other()

    async def sort_as_is(self):
        row_dict = self.rows
        as_is_dict = {}
        for row, values in row_dict.items():
            if not values:
                as_is_dict[row] = []
            else:
                if values[0] == "As is":
                    as_is_dict[row] = values
        self.as_is = as_is_dict

    async def sort_other(self):
        as_is = self.as_is
        for row in as_is.keys():
            if row in self.rows.keys():
                del self.rows[row]
            else:
                continue

    async def send_message(self) -> None:
        """постит данные"""
        for row, values in self.rows.items():
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
                else:
                    text = f"""{tegs}
<b>{header}</b>
{description}

Ссылка: <a href='{link}'> {link_text}</a>
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
            del self.rows[row]
            break


    async def send_as_is(self) -> None:

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
                else:
                    text = f"""{tegs}
<b>{header}</b>
{description}

Ссылка: <a href='{link}'> {link_text}</a>
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
            break

