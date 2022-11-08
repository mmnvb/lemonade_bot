from aiogram import Dispatcher
from aiogram.types import Message
from helper import bot
from asyncio import gather
from data_base.main_db import get_random_song_db, get_user_lang


async def give_song(msg: Message):
    await (audio := gather(get_random_song_db()))
    await bot.send_audio(msg.chat.id, audio.result()[0][0])


async def help_msg(msg: Message):
    await (lang := gather(get_user_lang(msg.from_user.id)))
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

    if lang.result()[0] == "RU":
        await msg.answer(ru_text)
    else:
        await msg.answer(eng_text)


def register_user(dp: Dispatcher):
    dp.register_message_handler(help_msg, commands='help', in_db=True)
    dp.register_message_handler(give_song, text='✨🎶')
