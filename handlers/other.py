from create_bot import dp
from aiogram import types


@dp.message_handler(content_types=['new_chat_members', 'new_chat_photo', 'left_chat_member', 'delete_chat_photo'])
async def chat_info(message: types.Message):
    await message.delete()
