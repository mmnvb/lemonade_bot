from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from misc.states import FsmPost
from data_base.main_db import get_all_users_db
from asyncio import gather, sleep

from aiogram.utils.exceptions import BotBlocked
from keyboards.admin_kb import admin_menu_kb


async def post_start(msg: Message):
    await msg.answer("📝Please send me the text of your post"
                     "\n\n<i>[ /cancel to cease it</i> ]")
    await FsmPost.text.set()


async def text_post(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['post_text'] = msg.text
    await msg.answer('🌄Great! Send a pic/ gif/ short video'
                     '\n\n[ <i>/cancel to cease it</i> ]')
    await FsmPost.media.set()


async def media_post(media: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['media_id'] = media.photo[0].file_id
            media_type = 'photo'
        except IndexError:
            try:
                data['media_id'] = media.video.file_id
                media_type = 'video'
            except AttributeError:
                data['media_id'] = media.animation.file_id
                media_type = 'gif'

        post_text = data['post_text']
        media_id = data['media_id']

        if media_type == 'photo':
            await media.answer_photo(media_id, caption=post_text)
        elif media_type == 'video':
            await media.answer_video(media_id, caption=post_text)
        elif media_type == 'gif':
            await media.answer_animation(media_id, caption=post_text)
        await media.answer("In order to post this message write <code>/post</code>"
                           "\n\n[ <i>/cancel to cease it</i> ]")
        await FsmPost.decide.set()


async def post(msg: Message, state: FSMContext):
    await (users := gather(get_all_users_db()))
    users = users.result()[0]
    await msg.answer(f'👷‍♂<i><b>Posting started... {0}/{(l := len(users))}</b></i>')
    block_counter = 0
    counter = 0
    for session in users:
        counter += 1
        try:
            await msg.bot.copy_message(session, msg.chat.id, msg.message_id-2)
        except BotBlocked:
            block_counter += 1
        await msg.bot.edit_message_text(f'👷‍♂<i><b>Posting started... {counter}/{l}</b></i>\n'
                                        f'🔒Bot was blocked: <code>{block_counter}</code>',
                                        msg.chat.id, msg.message_id+1)
        await sleep(1)
    await msg.answer(f"<b>🧾Results</b>\n\n"
                     f"✅Delivered: <i>{counter-block_counter}/{counter}</i>\n")
    await state.finish()


async def cancel_post(msg: Message, state: FSMContext):
    await msg.answer('Anyway, good job dude😉', reply_markup=admin_menu_kb)
    await state.finish()


def register_admin_post(dp: Dispatcher):
    dp.register_message_handler(post_start, is_admin=True, text='✍Post')
    dp.register_message_handler(cancel_post, state=FsmPost.states, commands='cancel')
    dp.register_message_handler(text_post, lambda msg: len(msg.text) < 1024,
                                state=FsmPost.text, content_types='text')
    dp.register_message_handler(media_post, state=FsmPost.media,
                                content_types=['photo', 'video', 'animation'])
    dp.register_message_handler(post, state=FsmPost.decide, commands='post')
