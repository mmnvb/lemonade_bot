from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from misc.states import FsmPost


async def post(msg: Message):
    await msg.reply("Please send me the text of your post")
    await FsmPost.text.set()


async def text_post(msg: Message, state=FSMContext):
    async with state.proxy() as data:
        data['post_text'] = msg.text
    await msg.reply('Great! Send a pic/ gif/ short video')
    await FsmPost.media.set()


async def media_post(media: Message, state=FSMContext):
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


def register_admin_post(dp: Dispatcher):
    dp.register_message_handler(post, is_admin=True, text='✍Post')
    dp.register_message_handler(text_post, state=FsmPost.text, content_types='text')
    dp.register_message_handler(media_post, state=FsmPost.media,
                                content_types=['photo', 'video', 'animation'])
