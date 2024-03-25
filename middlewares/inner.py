import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bd.tg_pass_bd import get_pass
from bd.tg_admin_bd import get_admin
from lexicon.lexicon import LEXICON_RU

logger = logging.getLogger(__name__)

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        logger.info(f'{user_id} вошел в SubscriptionMiddleware')
        db_host = data['db_host']
        db_database = data['db_database']
        db_user = data['db_user']
        db_password = data['db_password']
        db_port = data['db_port']
        if await get_pass(user_id, db_host, db_database, db_user, db_password, db_port):
            return await handler(event, data)
        else:
            await event.answer(LEXICON_RU['/pass'][0])
            logger.info(f'{user_id} не прошел в SubscriptionMiddleware')
            return

class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        logger.info(f'{user_id} вошел в AdminMiddleware')
        db_host = data['db_host']
        db_database = data['db_database']
        db_user = data['db_user']
        db_password = data['db_password']
        db_port = data['db_port']
        if await get_admin(user_id, db_host, db_database, db_user, db_password, db_port):
            return await handler(event, data)
        else:
            await event.answer('У вас нет прав Администратора')
            logger.info(f'{user_id} не прошел в AdminMiddleware')
            return