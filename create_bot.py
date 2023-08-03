from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv, find_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

logging.basicConfig(level=logging.INFO, filename="BotLastPost.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


if not load_dotenv(find_dotenv()):
    logging.warning('Не найден файл окружения или файл пустой, необходимо запустить скрипт settings.py')
    raise SystemExit(0)
load_dotenv(find_dotenv())
admin_id = os.environ.get("ADMIN").split(',')
time_message = os.environ.get("TIME")
storage = MemoryStorage()
bot = Bot(token=os.environ.get("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
