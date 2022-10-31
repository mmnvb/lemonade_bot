import aiogram.utils.exceptions
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import gather
from data_base.main_db import get_artists, search_artist_db, get_songs_db, search_song_db, get_song_db,\
    get_vibe_db, get_artist_db, get_song_title_db
from aiogram.types import ParseMode, Message, CallbackQuery
from aiogram.dispatcher import FSMContext

button = InlineKeyboardButton

admin_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('⬆Load track')],
        [KeyboardButton('💾Backup'), KeyboardButton("✍Post")],
        [KeyboardButton("⛏Edit")]],
    resize_keyboard=True,
    one_time_keyboard=True)


async def set_artist_kb(msg: Message):
    inline_artist_kb = InlineKeyboardMarkup(row_width=1).row(button(text='➕Add a new one', callback_data='add_artist'),
                                                             button(text='🔎Search', callback_data='search_artist'))
    await (artist := gather(get_artists(' ')))
    for i in artist.result()[0]:
        inline_artist_kb.add(button(text='👤'+i[0], callback_data=i[0]))
    inline_artist_kb.row(
        button(text='🔙Back', callback_data='back'),
        button(text='🏘To menu', callback_data='finish')
    )

    await msg.answer('Choose an artist🕺', reply_markup=inline_artist_kb)


async def get_artist_search_kb(msg: Message):
    inline_search_result_kb = InlineKeyboardMarkup(row_width=3)
    inline_search_result_kb.add(button(text='🔙Back', callback_data='artist_add_de_confirm'))
    inline_search_result_kb.insert(button(text='🔁𝙏𝙧𝙮 𝙖𝙜𝙖𝙞𝙣', callback_data='research_artist'))
    await (artists := gather(search_artist_db(msg.text)))
    for i in artists.result()[0]:
        inline_search_result_kb.add(button(text='👤'+i[0], callback_data=i[0]))
    await msg.answer('🔎Here is your results, choose one of them', reply_markup=inline_search_result_kb)


async def confirm_artist_add(msg: Message):
    inline_artist_confirm_kb = InlineKeyboardMarkup(row_width=2)
    inline_artist_confirm_kb.add(button(text='✅Sure', callback_data='artist_add_confirm'))
    inline_artist_confirm_kb.insert(button(text='❌Nope', callback_data='artist_add_de_confirm'))
    await msg.reply(f'<b>Are you sure</b> that\nyou want to add <code>{msg.text}</code>?',
                    reply_markup=inline_artist_confirm_kb,
                    parse_mode=ParseMode.HTML)


async def vibe_choose_kb(msg: Message):
    inline_vibe_kb = InlineKeyboardMarkup(row_width=1)
    inline_vibe_kb.add(
        button(text='⚡ｖｉｇｏｒｏｕｓ', callback_data='energy'),
        button(text='🤤ｃｈｉｌｌ', callback_data='chill'),
        button(text='😩ｓａｄ', callback_data='sad'),
        button(text='🔙Back', callback_data='back')
    )
    await msg.answer("Now choose track's mood🎭", reply_markup=inline_vibe_kb)


async def load_song_last_choice(msg: Message):
    inline_load_last = InlineKeyboardMarkup(row_width=1)
    inline_load_last.add(
        button(text='➕Add one more', callback_data='restart_loading'),
        button(text='🏘Go to menu', callback_data='finish')
    )
    await msg.answer('🥳Congrats!\nWhat are we going to do next?', reply_markup=inline_load_last)


async def list_of_songs(msg: Message, start=0, finish=10):
    inline_list_song = InlineKeyboardMarkup()
    inline_list_song.row(
        button(text='🔙Back', callback_data='back'),
        button(text='🔎Search', callback_data='search')
    )
    await (songs := gather(get_songs_db(start, finish)))
    for i in songs.result()[0]:
        t = i[0].lower().replace(i[1].lower(), '').replace("-", "").replace('  ', '').title()
        inline_list_song.add(
            button(text=f'{i[1]} - {t}', callback_data=i[2])
        )
    try:
        await msg.edit_text(f'Here is your list of songs🎶',
                            reply_markup=inline_list_song)
        await msg.edit_reply_markup(inline_list_song)

    except (aiogram.utils.exceptions.MessageCantBeEdited, aiogram.utils.exceptions.MessageToEditNotFound):
        await msg.answer(f'Here is your list of songs🎶',
                         reply_markup=inline_list_song)
    except aiogram.utils.exceptions.MessageNotModified:
        pass


async def get_song_search_kb(msg: Message):
    inline_search_s_result_kb = InlineKeyboardMarkup(row_width=3)
    inline_search_s_result_kb.add(button(text='🔙Back', callback_data='song_search_de_confirm'))
    inline_search_s_result_kb.insert(button(text='🔁𝙏𝙧𝙮 𝙖𝙜𝙖𝙞𝙣', callback_data='research_song'))
    await (songs := gather(search_song_db(msg.text)))
    for i in songs.result()[0]:
        t = i[0].lower().replace(i[1].lower(), '').replace("-", "").replace('  ', '').title()
        inline_search_s_result_kb.add(
            button(text=f'{i[1]} - {t}', callback_data=i[2])
        )
    await msg.answer('🔎Here is your results, choose one of them', reply_markup=inline_search_s_result_kb)


async def choose_song_tool(callback: CallbackQuery):
    inline_tool_choice = InlineKeyboardMarkup(row_width=2)
    inline_tool_choice.add(button('🔙Back', callback_data='edit_back'))
    inline_tool_choice.add(
        button('👤Artist🎙', callback_data='edit_artist'),
        button('🎭Mood', callback_data='edit_mood'),
        button('🗑Delete', callback_data='edit_delete')
    )
    await (track_id := gather(get_song_db(callback.data)))
    await callback.message.answer_audio(track_id.result()[0], reply_markup=inline_tool_choice,
                                        caption="🎵Just edit it")


async def current_mood_kb(callback: CallbackQuery):
    await (current_vibe := gather(get_vibe_db(callback.message.audio.title)))
    current_vibe = current_vibe.result()[0]
    inline_mood_change = InlineKeyboardMarkup(row_width=1)
    inline_mood_change.add(
        button(text='⚡ｖｉｇｏｒｏｕｓ ✅' if current_vibe == 'energy' else '⚡ｖｉｇｏｒｏｕｓ',
               callback_data='energy'),
        button(text='🤤ｃｈｉｌｌ ✅' if current_vibe == 'chill' else '🤤ｃｈｉｌｌ', callback_data='chill'),
        button(text='😩ｓａｄ ✅' if current_vibe == 'sad' else '😩ｓａｄ', callback_data='sad'),
        button(text='🔙Back', callback_data='vibe_art_change_back')
    )
    try:
        await callback.message.edit_reply_markup(inline_mood_change)
    except aiogram.utils.exceptions.MessageNotModified:
        await callback.answer('🟡It already has chosen')


async def back_to_tools_kb(callback: CallbackQuery):
    inline_tool_choice = InlineKeyboardMarkup(row_width=2)
    inline_tool_choice.add(button('🔙Back', callback_data='edit_back'))
    inline_tool_choice.add(
        button('👤Artist🎙', callback_data='edit_artist'),
        button('🎭Mood', callback_data='edit_mood'),
        button('🗑Delete', callback_data='edit_delete')
    )
    await callback.message.edit_reply_markup(inline_tool_choice)


async def delete_song_confirm(callback: CallbackQuery):
    inline_delete_confirm_kb = InlineKeyboardMarkup(row_width=2)
    inline_delete_confirm_kb.add(
        button('✅Sure', callback_data='delete_confirmed'),
        button('❌Nope', callback_data='delete_rejected')
    )
    await callback.message.edit_reply_markup(inline_delete_confirm_kb)


async def track_load_cancel_kb(msg: Message):
    inline_to_menu = InlineKeyboardMarkup()
    inline_to_menu.add(
        button(text='🏘To menu', callback_data='finish')
    )
    await msg.answer("𝐒𝐞𝐧𝐝 𝐦𝐞 𝐚 𝐬𝐨𝐧𝐠", reply_markup=inline_to_menu)


# edit artist
async def edit_artist_kb(callback: CallbackQuery):
    inline_artist_kb = InlineKeyboardMarkup(row_width=1).row(button(text='🔎Search', callback_data='search_artist'))
    await (artist := gather(get_artists('ORDER by ROWID DESC')))
    await (current := gather(get_artist_db(callback.message.audio.title)))
    for i in artist.result()[0]:
        inline_artist_kb.add(button(text='👤'+i[0] + ' ✅' if i[0] == current.result()[0] else '👤'+i[0],
                                    callback_data=i[0]))
    inline_artist_kb.row(
        button(text='🔙Back', callback_data='to_artist_tool')
    )
    await callback.message.edit_caption("🎵Just edit it")
    await callback.message.edit_reply_markup(inline_artist_kb)


# search artist
async def completed_artist_search(msg: Message, state=FSMContext):
    inline_search_result_kb = InlineKeyboardMarkup(row_width=3)
    inline_search_result_kb.add(button(text='🔙Back', callback_data='to_track_tool'))
    await (artists := gather(search_artist_db(msg.text)))
    async with state.proxy() as data:
        await (current := gather(get_artist_db(data['song'])))
    for i in artists.result()[0]:
        inline_search_result_kb.add(button(text='👤'+i[0] + ' ✅' if i[0] == current.result()[0] else '👤'+i[0],
                                           callback_data=i[0]))
    await (track_id := gather(get_song_title_db(data['song'])))
    await msg.answer_audio(track_id.result()[0], reply_markup=inline_search_result_kb, caption="🔎Here is your results")


# what to do with artist
async def artist_actions(callback: CallbackQuery):
    await callback.answer(callback.data)
    inline_action_choice = InlineKeyboardMarkup(row_width=1)
    inline_action_choice.add(
        button('💾Set this as artist', callback_data=f'set_{callback.data}'),
        button('❌Remove artist forever', callback_data=f'REmoVe_{callback.data}'),
        button(text='🔙Back', callback_data='to_track_tool')
    )
    await callback.message.edit_caption(f'What are you going to do with <code>{callback.data}</code>?',
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=inline_action_choice)
