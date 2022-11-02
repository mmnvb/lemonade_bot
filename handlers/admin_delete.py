from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from keyboards.admin_kb import list_of_songs, get_song_search_kb, choose_song_tool, current_mood_kb,\
    back_to_tools_kb, delete_song_confirm, edit_artist_kb, completed_artist_search, artist_actions
from handlers.admin_load import to_menu
from data_base.main_db import edit_vibe_db, delete_song_db, select_artist_db, remove_artist_db
from aiogram.dispatcher import FSMContext
from misc.states import FsmEdit


# list
async def start_editing(msg: Message):
    await list_of_songs(msg)
    await FsmEdit.song_choice.set()


# search
async def search_song(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("🔎Alright text me song's title")
    await FsmEdit.song_search.set()


async def get_search(msg: Message):
    await get_song_search_kb(msg)


# backs
async def to_start(callback: CallbackQuery):
    await start_editing(callback.message)


async def to_start_audio(callback: CallbackQuery):
    await callback.message.delete()
    await start_editing(callback.message)
    await callback.answer()


async def to_choose(callback: CallbackQuery):
    await back_to_tools_kb(callback)
    await callback.answer()


# tools
async def choose_tools(callback: CallbackQuery):
    await callback.message.delete()
    await FsmEdit.tools_choice.set()
    await choose_song_tool(callback)


async def change_mood(callback: CallbackQuery):
    await current_mood_kb(callback)
    await callback.answer()


async def rewrite_mood(callback: CallbackQuery):
    await edit_vibe_db(vibes=callback.data, title=callback.message.audio.title)
    await current_mood_kb(callback)
    await callback.answer()


# delete
async def delete_start(callback: CallbackQuery):
    await delete_song_confirm(callback)
    await callback.answer()


async def delete_confirmed(callback: CallbackQuery):
    await delete_song_db(callback.message.audio.title)
    await callback.answer('🟢Deleted successfully🗑')
    await to_start_audio(callback)


# edit artist
async def song_artist_edit(callback: CallbackQuery):
    await edit_artist_kb(callback)
    await callback.answer()


# artist search
async def artist_search(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['song'] = callback.message.audio.title
    await callback.message.delete()
    await callback.message.answer("🔎Alright text me artist's name")
    await FsmEdit.artist_search.set()


# back to tools
async def to_song_tools(callback: CallbackQuery):
    await FsmEdit.tools_choice.set()
    await edit_artist_kb(callback)
    await callback.answer()


# artist set / delete
async def artist_remove(callback: CallbackQuery):
    await remove_artist_db(callback.data[7::])
    await callback.answer(f'🟢{callback.data[7::]} was deleted🗑', show_alert=True)
    await to_song_tools(callback)


async def artist_set(callback: CallbackQuery):
    await select_artist_db(callback.data[4::], callback.message.audio.title)
    await callback.answer(f'✅{callback.data[4::]} was selected')
    await to_song_tools(callback)


def register_track_delete(dp: Dispatcher):
    dp.register_message_handler(start_editing, is_admin=True, text='⛏Edit')
    # queries
    dp.register_callback_query_handler(to_menu, text='back', state=FsmEdit.song_choice)
    dp.register_callback_query_handler(search_song, text='search', state=FsmEdit.song_choice)
    # search
    dp.register_message_handler(get_search, state=FsmEdit.song_search)
    dp.register_callback_query_handler(search_song, state=FsmEdit.song_search, text='research_song')
    dp.register_callback_query_handler(to_start, state=FsmEdit.song_search, text='song_search_de_confirm')
    # song's handler
    dp.register_callback_query_handler(choose_tools, state=[FsmEdit.song_search, FsmEdit.song_choice])
    # tool choice handler
    dp.register_callback_query_handler(to_start_audio, state=FsmEdit.tools_choice, text='edit_back')
    dp.register_callback_query_handler(change_mood, state=FsmEdit.tools_choice, text='edit_mood')
    dp.register_callback_query_handler(to_choose, state=FsmEdit.tools_choice,
                                       text=['vibe_art_change_back', 'delete_rejected'])
    # mood change handler
    dp.register_callback_query_handler(rewrite_mood, state=FsmEdit.tools_choice, text=['1', '2', '3'])
    # delete handler
    dp.register_callback_query_handler(delete_start, state=FsmEdit.tools_choice, text='edit_delete')
    dp.register_callback_query_handler(delete_confirmed, state=FsmEdit.tools_choice, text='delete_confirmed')
    # artist edit
    dp.register_callback_query_handler(song_artist_edit, state=FsmEdit.tools_choice, text='edit_artist')
    dp.register_callback_query_handler(to_choose, state=FsmEdit.tools_choice, text='to_artist_tool')
    # search
    dp.register_callback_query_handler(artist_search, state=FsmEdit.tools_choice, text='search_artist')
    dp.register_message_handler(completed_artist_search, state=FsmEdit.artist_search)
    dp.register_callback_query_handler(to_song_tools, state=[FsmEdit.artist_search, FsmEdit.tools_choice],
                                       text='to_track_tool')
    # handle artist click
    dp.register_callback_query_handler(artist_set, lambda c: c.data.startswith('set'),
                                       state=[FsmEdit.tools_choice, FsmEdit.artist_search])
    dp.register_callback_query_handler(artist_remove, lambda c: c.data.startswith('REmoVe'),
                                       state=[FsmEdit.tools_choice, FsmEdit.artist_search])
    dp.register_callback_query_handler(artist_actions, state=[FsmEdit.tools_choice, FsmEdit.artist_search])
