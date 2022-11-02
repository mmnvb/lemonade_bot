from asyncio import gather, sleep

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.admin_kb import set_artist_kb, get_artist_search_kb, confirm_artist_add, track_load_cancel_kb
from keyboards.admin_kb import load_song_last_choice, vibe_choose_kb
from handlers.admin_main import admin_menu_kb
from data_base.main_db import add_artist_db, add_song_db
from misc.states import FsmLoad
from data_base.main_db import search_artist_db


async def start_loading(msg: Message):
    await track_load_cancel_kb(msg)
    await FsmLoad.load.set()


async def load_track(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = msg.audio.file_id
        data['song'] = msg.audio.title
    await set_artist_kb(msg)
    await FsmLoad.artist.set()


# search
async def search_artist(callback: CallbackQuery):
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("🔎Alright text me artist's name")
    await callback.answer()
    await FsmLoad.search_artist_state.set()


async def get_search_result(msg: Message):
    await get_artist_search_kb(msg)


# adding
async def add_artist(callback: CallbackQuery):
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("📝Alright text me artist's name")
    await FsmLoad.add_artist_state.set()


async def save_artist(msg: Message, state=FSMContext):
    try:
        await (search_given := gather(search_artist_db(msg.text)))
        assert search_given.result()[0] == list()

        await confirm_artist_add(msg)
        async with state.proxy() as data:
            data['new_artist'] = msg.text
    except AssertionError:
        await msg.answer('🟡This artist already exists in the database')
        await sleep(3)
        await msg.bot.delete_message(msg.chat.id, msg.message_id+1)
        await set_artist_kb(msg)
        await FsmLoad.artist.set()


async def add_artist_de_confirm(callback: CallbackQuery):
    await callback.message.delete()
    await FsmLoad.artist.set()
    await set_artist_kb(callback.message)


async def add_artist_confirm(callback: CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        await add_artist_db(data['new_artist'])
        await callback.answer('🟢Success!', show_alert=True)
        await add_artist_de_confirm(callback)


# choose vibe
async def artist_writer(callback: CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['artist'] = callback.data
    await callback.answer(f'🟢{callback.data} selected')
    await callback.message.delete()
    await FsmLoad.vibe.set()
    await vibe_choose_kb(callback.message)


async def set_vibe(callback: CallbackQuery, state=FSMContext):
    await callback.answer('🟢Vibe selected')
    async with state.proxy() as data:
        data['vibe'] = callback.data
        # set some additional data
        data['date'] = str(callback.message.date)
        data['admin'] = f'{callback.from_user.first_name}:{callback.from_user.id}'
        try:
            data.pop('new_artist')
            data.pop('page_start')
            data.pop('page_finish')
        finally:
            await add_song_db(tuple(data.values()))
            await callback.message.delete()
            await callback.answer('💾Filled successfully')
            await load_song_last_choice(callback.message)


# backs
async def to_start(callback: CallbackQuery):
    await start_loading(callback.message)
    await callback.message.delete()


async def to_menu(callback: CallbackQuery, state=FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(f'😏Good job {callback.from_user.first_name}', reply_markup=admin_menu_kb)


def register_track_load(dp: Dispatcher):
    # main states
    dp.register_message_handler(start_loading, is_admin=True, text="⬆Load track")
    dp.register_message_handler(load_track, state=FsmLoad.load.state, content_types='audio')
    # load queries
    dp.register_callback_query_handler(search_artist, text='search_artist', state=FsmLoad.artist)
    dp.register_callback_query_handler(add_artist, text='add_artist', state=FsmLoad.artist)
    # search
    dp.register_message_handler(get_search_result, state=FsmLoad.search_artist_state)
    dp.register_callback_query_handler(search_artist, text='research_artist', state=FsmLoad.search_artist_state)
    # add artist
    dp.register_message_handler(save_artist, state=FsmLoad.add_artist_state)
    dp.register_callback_query_handler(
        add_artist_de_confirm,
        text='artist_add_de_confirm',
        state=[FsmLoad.add_artist_state, FsmLoad.search_artist_state])
    dp.register_callback_query_handler(add_artist_confirm, text='artist_add_confirm', state=FsmLoad.add_artist_state)
    # backs
    dp.register_callback_query_handler(to_start, state=FsmLoad.artist, text='back')
    dp.register_callback_query_handler(add_artist_de_confirm, state=FsmLoad.vibe, text='back')
    dp.register_callback_query_handler(to_start, state=FsmLoad.vibe, text='restart_loading')
    dp.register_callback_query_handler(to_menu, state=FsmLoad.vibe, text='finish')
    dp.register_callback_query_handler(to_menu, state=[FsmLoad.artist, FsmLoad.load], text='finish')
    # artist handler
    dp.register_callback_query_handler(artist_writer, state=[FsmLoad.artist, FsmLoad.search_artist_state])
    # vibe handler
    dp.register_callback_query_handler(set_vibe, state=FsmLoad.vibe)
