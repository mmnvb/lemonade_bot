import logging
import asyncio

from helper import dp
from data_base.main_db import db_start
from handlers.all import register_all
from handlers.admin_load import register_track_load
from handlers.admin_main import register_admin_request
from handlers.admin_delete import register_track_delete
from handlers.user import register_user
from handlers.admin_post import register_admin_post
from filters.admin import AdminFilter
from helper import bot

logger = logging.getLogger(__name__)


def register_all_filters(dispatcher):
    dispatcher.filters_factory.bind(AdminFilter)


def register_all_handlers(dispatcher):
    register_admin_request(dispatcher)
    register_admin_post(dispatcher)
    register_track_load(dispatcher)
    register_track_delete(dispatcher)
    register_user(dispatcher)
    register_all(dispatcher)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    await db_start()

    register_all_filters(dp)
    register_all_handlers(dp)
    # start
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
