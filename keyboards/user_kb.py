from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from data_base.main_db import check_user_db, get_user_lang
from asyncio import gather


user_kb_eng = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton('✨🎶')]],
    resize_keyboard=True)


inline_user_lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('🇷🇺RU', callback_data='RU')],
        [InlineKeyboardButton('🇬🇧ENG', callback_data='ENG')]
    ]
)


async def user_start(msg: Message):
    await (lang := gather(get_user_lang(msg.chat.id)))
    if lang.result()[0] == 'RU':
        await msg.answer('Привет, я найду подземные сокровища в мире западной музыки🫡💫', reply_markup=user_kb_eng)
    else:
        await msg.answer('Sup, i will find some undersea treasures for you🫡💫', reply_markup=user_kb_eng)


async def start_lang_kb(msg: Message):
    await (status := gather(check_user_db(msg.chat.id)))
    if status.result()[0] is True:
        await user_start(msg)
    else:
        await msg.answer('🇬🇧Choose your language\n🇷🇺Выберите свой язык', reply_markup=inline_user_lang)
