import asyncio
import random
from aiogram.utils import executor, exceptions
from create_bot import dp, bot, time_message
from aiogram import types
from data_base import sqlite_db
import handlers
import telebot
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(handlers=[RotatingFileHandler(filename="BotLastPost.log", maxBytes=100000, backupCount=7)],
                    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

async def send_message_telebot(time_interval: int):
    while True:
        sqlite_db.sql_start()
        x = random.randint(0, 10)
        for i in range(len(sqlite_db.db_chat())):
            db = sqlite_db.db_chat()
            bot1 = telebot.TeleBot(db[i][1])
            if db[i] != '':
                try:
                    bot1.delete_message(db[i][2], db[i][4])
                    logging.info(f'Сообщение №{db[i][4]} из группы {db[i][2]} удалено успешно')
                except telebot.apihelper.ApiTelegramException:
                    logging.error(f'{db[i][0]} Ошибка удаления, {db[i][2]} возможно нету еще данных для удаления')
            else:
                logging.warning(f'db[i][2] пустой ИД')
            try:
                a = bot1.send_message(db[i][2], db[i][3], parse_mode='HTML', disable_web_page_preview=True).message_id
                logging.info(f'Сообщение отправилось в группу №{db[i][2]} успешно.')
                sqlite_db.update_last_message(db[i][2], a)
            except telebot.apihelper.ApiTelegramException:
                logging.error(f'Ошибка отправки, {db[i][0]} возможно не является админом группы {db[i][2]}')
            x_m = random.randint(3, 6)
            await asyncio.sleep(x_m)
        await asyncio.sleep(time_interval + x)


async def on_startup(_):
    await bot.set_my_commands([
        types.BotCommand("/start", "Запустить бота"),
        types.BotCommand("/add_chat", "Добавить чат (группу)"),
    ], types.bot_command_scope.BotCommandScopeAllPrivateChats())
    logging.info('Бот вышел в онлайн')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_message_telebot(int(time_message)))
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
