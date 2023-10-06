# инициализируем необзходимые библиотеки
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from dotenv import main
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

# Загрузка переменных среды из файла .env
main.load_dotenv()

# Использование переменных среды
token = os.getenv('bot_token')
adminid = os.getenv('admin_id');

# Объект бота
bot = Bot(token);
# Диспетчер
dp = Dispatcher(bot, storage=storage)
