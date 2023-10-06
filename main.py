# инициализируем необзходимые библиотеки
import json
from aiogram import Dispatcher, types
from configdan import *
from aiogram.types import Message, ParseMode
from aiogram.utils import markdown, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from asyncio import sleep
import datetime

# Загрузка расписания из файла
with open('schedule.json', 'r', encoding='utf-8') as schedule_file:
    schedule = json.load(schedule_file)

async def get_user_status(user_id, chat_id):
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        status = chat_member.status
        return status
    except Exception as e:
        print(f"Ошибка при получении статуса пользователя: {e}")
        return None

# Функция для обновления переменной
def get_week_parity():
    # Получение текущей даты и времени
    current_time = datetime.datetime.now()

    # Получение даты 1 января текущего года
    start_of_year = datetime.datetime(current_time.year, 1, 1)

    # Вычисление разницы в днях между текущей датой и 1 января
    days_difference = (current_time - start_of_year).days

    # Определение дня недели 1 января
    day_of_week = start_of_year.weekday()

    # Вычисление номера недели с учетом дня недели 1 января
    week_number = (days_difference + day_of_week) // 7

    # Определение четности недели
    week_parity = "ЧЕТНАЯ" if week_number % 2 == 0 else "НЕЧЕТНАЯ"

    return ("НЕ" + week_parity if week_number % 2 != 0 else week_parity) + " НЕДЕЛЯ"

# Регистрация и меню
@dp.message_handler(commands=['start'])
async def client_start(message: types.Message):
    user_id = message.from_user.id
    formatted_text = f"""Привет, я Бот помощи для группы. 
Чем могу помочь?"""
    await message.answer(formatted_text)


# Функция для периодической проверки переменной
def get_today_and_tomorrow():
    # Получение сегодняшней даты
    today = datetime.date.today()

    # Определение сегодняшнего дня недели (0 - понедельник, 6 - воскресенье)
    today_weekday = today.weekday()

    # Определение имени сегодняшнего дня недели
    days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    today_name = days_of_week[today_weekday]

    # Получение завтрашней даты
    tomorrow = today + datetime.timedelta(days=1)

    # Определение завтрашнего дня недели
    tomorrow_weekday = tomorrow.weekday()

    # Определение имени завтрашнего дня недели
    tomorrow_name = days_of_week[tomorrow_weekday]

    return today, today_name, tomorrow, tomorrow_name

today_date, today_name, tomorrow_date, tomorrow_name = get_today_and_tomorrow()
chetnoctynedely = get_week_parity()

# Обработчик текстовых сообщений
@dp.message_handler(commands=['today_name'])
async def say_hello(message: types.Message):
    # Отправляем ответное сообщение
    await message.reply(f"Сегодня {today_name}")

# Обработчик текстовых сообщений
@dp.message_handler(commands=['tomorrow_name'])
async def say_hello(message: types.Message):
    # Отправляем ответное сообщение
    await message.reply(f"Завтра {tomorrow_name}")

# Обработчик текстовых сообщений
@dp.message_handler(commands=['schedule_for_today'])
async def say_hello(message: types.Message):
    chat_id = message.chat.id
    response_text = schedule[chetnoctynedely][today_name]  # Используйте переменные из вашего кода
    await bot.send_message(chat_id, response_text)

# Обработчик текстовых сообщений
@dp.message_handler(commands=['schedule_for_tomorrow'])
async def schedule_for_tomorrow(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely][tomorrow_name]  # Используйте переменные из вашего кода
    await bot.send_message(chat_id, response_text)

# Обработчик команды /monday
@dp.message_handler(commands=['monday'])
async def schedule_for_monday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['понедельник']
    await bot.send_message(chat_id, response_text)
            
# Обработчик команды /tuesday
@dp.message_handler(commands=['tuesday'])
async def schedule_for_tuesday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['вторник']
    await bot.send_message(chat_id, response_text)

@dp.message_handler(commands=['wednesday'])
async def schedule_for_tuesday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['среда']
    await bot.send_message(chat_id, response_text)
            
@dp.message_handler(commands=['thursday'])
async def schedule_for_tuesday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['четверг']
    await bot.send_message(chat_id, response_text)
            
@dp.message_handler(commands=['friday'])
async def schedule_for_tuesday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['пятница']
    await bot.send_message(chat_id, response_text)

@dp.message_handler(commands=['saturday'])
async def schedule_for_tuesday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['суббота']
    await bot.send_message(chat_id, response_text)

@dp.message_handler(commands=['sunday'])
async def schedule_for_tuesday(message: types.Message):
    chat_id = message.chat.id  # Идентификатор чата
    response_text = schedule[chetnoctynedely]['воскресенье']
    await bot.send_message(chat_id, response_text)


# Создайте словарь для сопоставления должностей
role_mapping = {
    'administrator': 'Админ',
    'member': 'Юзер'
}

@dp.message_handler(commands=['status'])
async def get_status(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    status = await get_user_status(user_id, chat_id)
    
    if status:
            status = role_mapping.get(status, status)
            await message.reply(f"""Должность: {status}""")
    else:
        await message.reply("Не удалось получить должность пользователя.")

# Обработчик команды /орелрешка
@dp.message_handler(commands=['coin'])
async def flip_coin_command(message: types.Message):
    # Выбираем случайное значение "Орел" или "Решка"
    result = random.choice(["Орел", "Решка"])
    await message.answer(f"Внимание, выпал(а) {result}")

# Обработчик команды /орелрешка
@dp.message_handler(commands=['dice'])
async def flip_coin_command(message: types.Message):
    result = random.choice(["1", "2", "3", "4", "5", "6"])
    await message.answer(f"Внимание, выпал(а) {result}")

# Обработчик команды /feedback с аргументами
@dp.message_handler(commands=['feedback'])
async def feedback_command(message: types.Message):
    # Проверяем, есть ли аргументы команды
    if message.get_args():
        feedback_text = message.get_args()
        # Отправляем обратную связь админу
        await bot.send_message(adminid, f"Обратная связь от пользователя (ID: {message.from_user.id}):\n\n{feedback_text}")
        
        # Отправляем подтверждение пользователю
        await message.reply("Спасибо за вашу обратную связь! Ваше предложение было отправлено администратору.")
    else:
        await message.reply("Пожалуйста, введите ваше сообщение после команды /feedback.")

#запуск бота
async def on_startup(_):
    await bot.send_message(adminid, f"Student Group Bot вышел в онлайн")
    print('Student Group Bot вышел в онлайн')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, loop=loop)
