import datetime
import time

FORMAT = '%H:%M:%S'
WEIGHT = 75
HEIGHT = 175
K_1 = 0.035
K_2 = 0.029
STEP_M = 0.65

storage_data = {}


def check_correct_data(data):
    """Проверка корректности полученного пакета."""
    if len(data) != 2 or None in data:
        return False
    return True


def check_correct_time(time):
    """Проверка корректности параметра времени."""
    if len(storage_data) > 0 and max(storage_data) >= time:
        return False
    return True


def get_step_day(steps):
    """Получить количество пройденных шагов за этот день."""
    return sum(storage_data.values()) + steps 
    

def get_distance(steps):
    """Получить дистанцию пройденного пути в км."""
    return steps * STEP_M / 1000


def get_spent_calories(dist, current_time):
    """Получить значения потраченных калорий."""
    time_spent = float(f'{current_time.tm_hour}.{current_time.tm_min*100//60}')
    speed = dist / time_spent
    calories_per_min = K_1 * WEIGHT + (speed ** 2 / HEIGHT) * K_2 * WEIGHT
    return calories_per_min * (time_spent * 60)


def get_achievement(dist):
    """Получить поздравления за пройденную дистанцию."""
    if dist >= 6.5:
        return 'Отличный результат! Цель достигнута.'
    elif dist >= 3.9:
        return 'Неплохо! День был продуктивным.'
    elif dist >= 2:
        return 'Маловато, но завтра наверстаем!'
    else:
        return 'Лежать тоже полезно. Главное — участие, а не победа!' 


def show_message(c_time, d_steps, d_dist, cals, achiev):
    print(f'''\nВремя: {c_time}.
Количество шагов за сегодня: {d_steps}.
Дистанция составила {d_dist:.2f} км.
Вы сожгли {cals:.2f} ккал.
{achiev}\n''')


def accept_package(data):
    """Обработать пакет данных."""
    if not check_correct_data(data):
        return 'Некорректный пакет'
    timestr, steps = data
    pack_time =  time.strptime(timestr, FORMAT)
    if not check_correct_time(pack_time):
        return 'Некорректное значение времени'
    day_steps = get_step_day(steps)
    dist = get_distance(day_steps)
    spent_calories = get_spent_calories(dist, pack_time)
    achievement = get_achievement(dist)
    message_data = {
        'c_time': time.strftime(FORMAT, pack_time),
        'd_steps': day_steps,
        'd_dist': dist,
        'cals': spent_calories,
        'achiev': achievement,
    }
    show_message(**message_data)
    storage_data[pack_time] = steps
    return storage_data


package_0 = ('2:00:01', 505)
package_1 = (None, 3211)
package_2 = ('9:36:02', 15000)
package_3 = ('9:36:02', 9000)
package_4 = ('8:01:02', 7600)

accept_package(package_0)
accept_package(package_1)
accept_package(package_2)
accept_package(package_3)
accept_package(package_4)
