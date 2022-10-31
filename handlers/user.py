from aiogram import Dispatcher
from aiogram.types import Message
from helper import bot
from asyncio import gather
from data_base.main_db import get_random_song_db


async def give_song(msg: Message):
    await (audio := gather(get_random_song_db()))
    await bot.send_audio(msg.chat.id, audio.result()[0][0])


def register_user(dp: Dispatcher):
    dp.register_message_handler(give_song, text='✨🎶')
