import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from asyncio import gather
from data_base.main_db import check_user_db


class UserInDB(BoundFilter):
    key = 'in_db'

    def __init__(self, in_db: typing.Optional[bool] = None):
        self.in_db = in_db

    async def check(self, obj):
        if self.in_db is None:
            return False

        telegram_user: types.User = obj.from_user
        await (answer := gather(check_user_db(user_id=telegram_user.id)))

        try:
            assert answer.result()[0] is True
            return True
        except AssertionError:
            return False
