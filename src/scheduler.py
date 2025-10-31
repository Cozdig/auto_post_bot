
from datetime import datetime, date, time
from api_handler import get_info


schedule = [
{'day' : 1, 'time_1' : '10:00', 'time_2' : '13:00'},
{'day' : 2, 'time_1' : '10:00', 'time_2' : '12:00'},
{'day' : 3, 'time_1' : '10:00', 'time_2' : '14:00'},
{'day' : 4, 'time_1' : '10:00', 'time_2' : '15:00'}
]

schedule_rest = [
    {'day' : 0},
    {'day' : 5},
    {'day' : 6}
]
def check_new_posts():
    now = datetime.now()
    day = now.weekday()
    if day == 1:
        all_info, last_row = get_info()
    else:
        pass
    print(day)

def do_posts():
    now = datetime.now()
    day = now.weekday()
    for times in schedule:
        for date_, time_ in times.keys():
            if day == date_:
                continue
                #сделать выкладывание постов по времени из schedule
            else:
                #сделать проверку выходных дней
                break

# сделать файл с форматированием в читаемый текст из списка словарей
# сделать проверку на текущий день и чекание постов
if __name__ == "__main__":
    check_new_posts()