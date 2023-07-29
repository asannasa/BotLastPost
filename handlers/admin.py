from aiogram import types
from create_bot import dp, admin_id, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from data_base import sqlite_db
from keyboards import admin_kb


class FSMAdmin(StatesGroup):
    nameBOT = State()
    tokenBOT = State()
    chatID = State()
    text = State()


class FSMText(StatesGroup):
    nameBot = State()
    text = State()


class FSMDelete(StatesGroup):
    nameBot = State()


text_start = """<b>Привет</b>\nЭто бот последнего сообщения <b>Last Post Bot</b>. """ \
                 """Чтобы добавить нового бота нажмите <b>"Добавить бота"</b> или отправьте команду /addnewbot"""


@dp.message_handler(user_id=admin_id, chat_id=admin_id, commands=['start', 'allbots'])
async def command_start(message: types.Message):
    await message.delete()
    await message.answer(text_start, reply_markup=admin_kb.get_inline_button())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.delete_message(message.chat.id, message.message_id-1)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id, text_start, reply_markup=admin_kb.get_inline_button())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, commands=['addnewbot'], state=None)
async def command_add_chat(message: types.Message):
    await message.delete()
    await FSMAdmin.nameBOT.set()
    await bot.send_message(message.chat.id, 'Введите имя бота:', reply_markup=admin_kb.get_cancel_kb())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, state=FSMAdmin.nameBOT)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nameBOT'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи токен бота:", reply_markup=admin_kb.get_cancel_kb())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, state=FSMAdmin.tokenBOT)
async def load_token(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tokenBOT'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи ИД чата(группы):", reply_markup=admin_kb.get_cancel_kb())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, state=FSMAdmin.chatID)
async def load_chat_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chatID'] = int(message.text)
    await FSMAdmin.next()
    await message.reply("Введи текст:", reply_markup=admin_kb.get_cancel_kb())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, state=FSMAdmin.text)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.html_text
    await sqlite_db.add_chat_text(data)
    await message.reply('Бот успешно добавлен')
    await state.finish()
    await bot.send_message(message.chat.id, text_start, reply_markup=admin_kb.get_inline_button())


@dp.callback_query_handler(Text(startswith='edit_'), state=None)
async def call_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await FSMText.nameBot.set()
    async with state.proxy() as data:
        data['nameBOT'] = callback.data.split("_")[1]
    await FSMText.next()
    await callback.message.answer(f"Введи текст:", reply_markup=admin_kb.get_cancel_kb())


@dp.message_handler(user_id=admin_id, chat_id=admin_id, state=FSMText.text)
async def save_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.html_text
    await sqlite_db.save_text(data)
    await state.finish()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.delete_message(message.chat.id, message.message_id-1)
    await bot.send_message(message.chat.id, text_start, reply_markup=admin_kb.get_inline_button())


@dp.callback_query_handler(Text(startswith='delete_'), state=None)
async def call_delete(callback: CallbackQuery, state: FSMContext):
    await FSMDelete.nameBot.set()
    async with state.proxy() as data:
        data['nameBOT'] = callback.data.split("_")[1]
    await sqlite_db.delete_bot(data)
    await state.finish()
    await bot.send_message(callback.message.chat.id, text_start, reply_markup=admin_kb.get_inline_button())
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@dp.callback_query_handler(Text(equals='cancel'))
async def call_home(callback: CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.message.chat.id, text_start, reply_markup=admin_kb.get_inline_button())


@dp.callback_query_handler(user_id=admin_id, chat_id=admin_id)
async def call_edit_bot(callback: CallbackQuery):
    if callback.data in sqlite_db.list_bot():
        await callback.message.delete()
        await callback.message.answer(text=f'Редактировать или удалить бота по имени <b>{callback.data}</b>:',
                                      reply_markup=admin_kb.get_keyboard_edit(callback.data))
