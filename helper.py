from aiogram import Dispatcher, Bot
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
