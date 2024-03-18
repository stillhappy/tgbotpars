import asyncio
import time
import os
from aiogram import Bot
from aiogram.types import FSInputFile
from bd.tg_users_bd import get_pass_users_with_settings
from bd.bd_func import get_json_cofs
from services.graphic import get_data_for_graph
from services.del_papka import clear_folder
import logging

async def send_message_with_photo(bot, user_ids, photo_path):
    avoid_list = ['PGL Major Copenhagen']
    for user_id in user_ids:
        list_tags = photo_path.lstrip('photos\\').split('_')
        caption = (f'Турнир: <b>{list_tags[-3]}</b>\n'
                   f'Матч: <b>{list_tags[-2]} - {list_tags[-1].rstrip('.png')}</b>\n'
                   f'Прогруз(<b>{list_tags[0][1:]}</b>):\n'
                   f'<b>{list_tags[-4].replace("-", " - ")}</b> ➡️ <b>{list_tags[-5].replace("-", " - ")}</b>')
        if list_tags[1].lower().replace(' ', '') in user_id[1] and list_tags[0][1:].lower() in user_id[2] and float(list_tags[2]) >= float(user_id[3]) and list_tags[-3].strip() not in avoid_list:
            await bot.send_photo(chat_id=user_id[0], photo=FSInputFile(photo_path), caption=caption)

async def send_messages(bot, user_ids, photo_list):
    logger = logging.getLogger(__name__)
    logger.info('Выполнение рассылки')
    for photo_path in photo_list:
        logger.info(f"{photo_path}")
        await send_message_with_photo(bot, user_ids, photo_path)
        # f"photos/{bk}_{game}_{round(difference, 2)}_({coef1[-1]}-{coef2[-1]})_({coef1[-2]}-{coef2[-2]})_{tour_name}.png"

def scheduled_messaging(bot_token, interval, db_host, db_database, db_user, db_password, db_port):
    while True:
        user_ids = get_pass_users_with_settings(db_host, db_database, db_user, db_password, db_port)
        get_json_cofs(db_host, db_database, db_user, db_password, db_port)
        clear_folder()
        get_data_for_graph()
        photo_list = [os.path.join('photos', filename) for filename in os.listdir('photos')]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot = Bot(token=bot_token, parse_mode='HTML')
        try:
            loop.run_until_complete(send_messages(bot, user_ids, photo_list))
        finally:
            loop.run_until_complete(bot.session.close())
        time.sleep(interval)