from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards.user_kb import start_lang_kb, user_start
from data_base.main_db import register_user_db


async def start_lang(msg: Message):
    await start_lang_kb(msg)


async def register_user(callback: CallbackQuery):
    await register_user_db(callback.message.chat.id, callback.data)
    await callback.answer('Вы выбрали русский' if callback.data == '1' else 'You selected English')
    await callback.message.delete()
    await user_start(callback.message)


async def restart(msg: Message, state: FSMContext):
    await msg.answer('🟢Restarted')
    await state.finish()


def register_all(dp: Dispatcher):
    dp.register_message_handler(restart, commands='restart', state="*")
    dp.register_message_handler(start_lang, commands=['start', 'register'])
    dp.register_callback_query_handler(register_user, text=['1', '0'])
