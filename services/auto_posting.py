import asyncio
import time
import os
from aiogram.exceptions import TelegramForbiddenError
from aiogram import Bot
from aiogram.types import FSInputFile
from bd.tg_users_bd import get_pass_users_with_settings
from bd.bd_func import get_json_cofs
from services.graphic import get_data_for_graph
from services.del_papka import clear_folder
import logging
from datetime import datetime, timedelta

async def send_message_with_photo(bot, user_ids, photo_path, list_pass_end, logger):
    avoid_list = ['PGL Major Copenhagen']
    for user_id in user_ids:
        list_tags = photo_path.lstrip('photos\\').split('_')
        caption = (f'Турнир: <b>{list_tags[-3]}</b>\n'
                   f'Матч: <b>{list_tags[-2]} - {list_tags[-1].rstrip('.png')}</b>\n'
                   f'Прогруз(<b>{list_tags[0][1:]}</b>):\n'
                   f'<b>{list_tags[-4].replace("-", " - ")}</b> ➡️ <b>{list_tags[-5].replace("-", " - ")}</b>')
        if list_tags[1].lower().replace(' ', '') in user_id[1] and list_tags[0][1:].lower() in user_id[2] and float(list_tags[2]) >= float(user_id[3]) and list_tags[-3].strip() not in avoid_list:
            try:
                await bot.send_photo(chat_id=user_id[0], photo=FSInputFile(photo_path), caption=caption)
            except TelegramForbiddenError:
                logger.exception(f"Bot is blocked by user {user_id[0]}")
                continue
        if list_pass_end and user_id[0] in list_pass_end:
            await bot.send_message(chat_id=user_id[0], text='🚨<b>Сегодня у вас истекает подписка</b>🚨')
            if user_id[5]:
                await bot.send_message(chat_id=461491549, text=f'🚨<b>Сегодня у @{user_id[5]} истекает подписка</b>🚨')
                await bot.send_message(chat_id=677134128, text=f'🚨<b>Сегодня у @{user_id[5]} истекает подписка</b>🚨')
            else:
                await bot.send_message(chat_id=461491549, text=f'🚨<b>Сегодня у {user_id[6]} истекает подписка</b>🚨')
                await bot.send_message(chat_id=677134128, text=f'🚨<b>Сегодня у {user_id[6]} истекает подписка</b>🚨')
            list_pass_end.remove(user_id[0])

async def send_messages(bot, user_ids, photo_list, list_pass_end):
    logger = logging.getLogger(__name__)
    logger.info('Выполнение рассылки')
    for photo_path in photo_list:
        logger.info(f"{photo_path}")
        await send_message_with_photo(bot, user_ids, photo_path, list_pass_end, logger)
        # f"photos/{bk}_{game}_{round(difference, 2)}_({coef1[-1]}-{coef2[-1]})_({coef1[-2]}-{coef2[-2]})_{tour_name}.png"

def scheduled_messaging(bot_token, interval, db_host, db_database, db_user, db_password, db_port):
    while True:
        list_pass_end = []
        bot = Bot(token=bot_token, parse_mode='HTML')
        user_ids = get_pass_users_with_settings(db_host, db_database, db_user, db_password, db_port)
        current_date = datetime.now() + timedelta(hours=3)
        sr = datetime.strptime('2024-03-20 12:30:00', '%Y-%m-%d %H:%M:%S')
        sr2 = sr + timedelta(minutes=5)
        if current_date.hour == sr.hour and sr.minute <= current_date.minute <= sr2.minute:
            for user_id in user_ids:
                if user_id[4]:
                    end_pass = user_id[4]
                    if current_date.month == end_pass.month and current_date.day == end_pass.day and current_date.year == end_pass.year:
                        list_pass_end.append(user_id[0])
        get_json_cofs(db_host, db_database, db_user, db_password, db_port)
        clear_folder()
        get_data_for_graph()
        photo_list = [os.path.join('photos', filename) for filename in os.listdir('photos')]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(send_messages(bot, user_ids, photo_list, list_pass_end))
        finally:
            loop.run_until_complete(bot.session.close())
        time.sleep(interval)