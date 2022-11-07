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
        [InlineKeyboardButton('🇷🇺RU', callback_data='1')],
        [InlineKeyboardButton('🇬🇧ENG', callback_data='0')]
    ]
)


async def user_start(msg: Message):
    await (lang := gather(get_user_lang(msg.chat.id)))
    ru_text = f"<b>Привет {msg.from_user.first_name}👋</b>\n\n" \
              f"🔥В этом боте собраны:\n\n" \
              f"<i>- Уникальные треки\n" \
              f"- Эдиты\n" \
              f"- Невышедшие демки\n" \
              f"🪐️И многое другое от западных артистов🤑</i>\n\n" \
              f"" \
              f"<b>Просто жми на кнопку и получай сок</b>🧃"

    eng_text = f"<b>Hi {msg.from_user.first_name}👋</b>\n\n" \
               f"🔥Our team has collected:\n\n" \
               f"<i>- Unique tracks\n" \
               f"- Edits\n" \
               f"- Unreleased demos\n" \
               f"🪐️And much more from your artists for you🤑</i>\n\n" \
               f"" \
               f"<b>Just click on the button and get the juice</b>🧃"
    if lang.result()[0] == 'RU':
        await msg.answer(ru_text, reply_markup=user_kb_eng)
    else:
        await msg.answer(eng_text, reply_markup=user_kb_eng)


async def start_lang_kb(msg: Message):
    await (status := gather(check_user_db(msg.chat.id)))
    if status.result()[0] is True:
        await user_start(msg)
    else:
        await msg.answer('🇬🇧Choose your language\n🇷🇺Выберите свой язык', reply_markup=inline_user_lang)
