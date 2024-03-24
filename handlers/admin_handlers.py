from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command
from keyboards.settings_kb import create_users_keyboard
from bd.tg_admin_bd import get_status_users, get_admin, give_pass, del_pass, update_pass

router = Router()

@router.message(Command(commands='users'))
async def send_pass_users(message: Message, db_host, db_database, db_user, db_password, db_port):
    await update_pass(db_host, db_database, db_user, db_password, db_port)
    await message.answer(
        text=LEXICON_RU[message.text],
        reply_markup=create_users_keyboard(await get_status_users(db_host, db_database, db_user, db_password, db_port))
    )


@router.callback_query(F.data.endswith(':0'))
async def give_pass_kb(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await give_pass(callback.data, db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_reply_markup(reply_markup=create_users_keyboard(await get_status_users(db_host, db_database, db_user, db_password, db_port)))

@router.callback_query(F.data.endswith(':1'))
async def del_pass_kb(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await del_pass(callback.data, db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_reply_markup(reply_markup=create_users_keyboard(await get_status_users(db_host, db_database, db_user, db_password, db_port)))