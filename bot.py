import asyncio
import logging
import threading
import time

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from handlers import user_handlers, pass_handlers, admin_handlers, other_handlers, parser_handlers
from keyboards.main_menu import set_main_menu
from services.auto_posting import scheduled_messaging
from middlewares.inner import AdminMiddleware, SubscriptionMiddleware

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()
    await set_main_menu(bot)
    dp.workflow_data.update({'db_host': config.db.db_host,
                             'db_database': config.db.database,
                             'db_user': config.db.db_user,
                             'db_password': config.db.db_password,
                             'db_port': config.db.db_port,
                             'admin_ids': config.tg_bot.admin_ids})
    subscription_middleware = SubscriptionMiddleware()
    admin_middleware = AdminMiddleware()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(pass_handlers.router)
    dp.include_router(parser_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)

    pass_handlers.router.message.middleware(subscription_middleware)
    pass_handlers.router.callback_query.middleware(subscription_middleware)
    parser_handlers.router.message.middleware(subscription_middleware)
    parser_handlers.router.callback_query.middleware(subscription_middleware)
    admin_handlers.router.message.middleware(admin_middleware)
    admin_handlers.router.callback_query.middleware(admin_middleware)

    interval = 210
    threading.Thread(target=scheduled_messaging, args=(config.tg_bot.token, interval, config.db.db_host, config.db.database, config.db.db_user, config.db.db_password, config.db.db_port)).start()
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())