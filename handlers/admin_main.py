from aiogram.types import Message
from aiogram import Dispatcher
from helper import bot
from keyboards.admin_kb import admin_menu_kb


async def admin_menu(msg: Message):
    await msg.reply(f'✅Admin was verified 👨‍💻{msg.from_user.first_name}', reply_markup=admin_menu_kb)


async def backup(msg: Message):
    await bot.send_document(msg.chat.id, open('memory.db', 'rb'), caption=f'backup for {msg.date}')


def register_admin_request(dp: Dispatcher):
    dp.register_message_handler(admin_menu, is_admin=True, commands='admin')
    dp.register_message_handler(backup, is_admin=True, text='💾Backup')
