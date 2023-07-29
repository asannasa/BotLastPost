from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base import sqlite_db


def get_cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('/cancel'))
    return kb


def get_inline_button():
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for i in range(len(sqlite_db.db_chat())):
        inline_kb.insert(InlineKeyboardButton(text=sqlite_db.db_chat()[i][0], callback_data=sqlite_db.db_chat()[i][0]))
    # if len(sqlite_db.db_chat()) > 10:
    #     inline_kb.add(InlineKeyboardButton(text='Следующий >>', callback_data='page_2'))
    return inline_kb


def get_keyboard_edit(name: str):
    b = sqlite_db.db_chat_bot(name)[0][0]
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.insert(InlineKeyboardButton(text='Редактировать текст', callback_data=f'edit_{b}'))
    inline_kb.insert(InlineKeyboardButton(text='Удалить бота', callback_data=f'delete_{b}'))
    inline_kb.insert(InlineKeyboardButton(text='Вернуться к списку ботов', callback_data='cancel'))
    return inline_kb
