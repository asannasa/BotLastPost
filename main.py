import asyncio
import random
from aiogram.utils import executor
from create_bot import dp, bot, time_message
from aiogram import types
from data_base import sqlite_db
import handlers
import telebot
import logging

logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

loop = asyncio.get_event_loop()


async def send_message_telebot(time: int):
    while True:
        x = random.randint(0, 10)
        for i in range(len(sqlite_db.db_chat())):
            db = sqlite_db.db_chat()
            bot1 = telebot.TeleBot(db[i][1])
            if db[i] != '':
                try:
                    bot1.delete_message(db[i][2], db[i][4])
                except telebot.apihelper.ApiTelegramException:
                    logging.error(f'{db[i][0]} Ошибка удаления, {db[i][2]} возможно нету еще данных для удаления')
            else:
                logging.warning(f'db[i][2] пустой ИД')

            try:
                a = bot1.send_message(db[i][2], db[i][3], parse_mode='HTML', disable_web_page_preview=True).message_id
                sqlite_db.update_last_message(db[i][2], a)
            except telebot.apihelper.ApiTelegramException:
                logging.error(f'Ошибка отправки, {db[i][0]} возможно не является админом группы {db[i][2]}')
            x_m = random.randint(3, 6)
            await asyncio.sleep(x_m)
        await asyncio.sleep(time + x)


async def on_startup(_):
    sqlite_db.sql_start()
    await bot.set_my_commands([
        types.BotCommand("/start", "Запустить бота"),
        types.BotCommand("/add_chat", "Добавить чат (группу)"),
    ], types.bot_command_scope.BotCommandScopeAllPrivateChats())
    logging.info('Бот вышел в онлайн')


if __name__ == '__main__':
    sqlite_db.sql_start()
    loop.create_task(send_message_telebot(int(time_message)))
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
