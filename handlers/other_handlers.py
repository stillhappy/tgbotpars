from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON_RU
from keyboards.settings_kb import create_settings_keyboard, create_edit_keyboard, create_kb_params, create_kb_edit_params, edit_kb_edit_params_add, edit_kb_edit_params_del, edit_kb_edit_params_pro
from bd.tg_users_bd import get_users, get_status_pass, get_info_settings, edit_params_del, edit_params_add, edit_params_pro

# Инициализируем роутер уровня модуля
router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message, db_host, db_database, db_user, db_password, db_port, admin_ids):
    await message.answer(text=LEXICON_RU['/start'])
    get_users(message, db_host, db_database, db_user, db_password, admin_ids, db_port)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(Command(commands='pass'))
async def process_help_command(message: Message, db_host, db_database, db_user, db_password, db_port):
    await message.answer(text=LEXICON_RU['/pass'][get_status_pass(message, db_host, db_database, db_user, db_password, db_port)])

@router.message(Command(commands='settings'))
async def process_settings_command(message: Message):
    await message.answer(
        text=LEXICON_RU[message.text],
        reply_markup=create_settings_keyboard()
    )

@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['cancel_text'])
    await callback.answer()

@router.callback_query(F.data.in_(['games', 'bookies', 'progruz']))
async def process_settings_param(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_kb_params(get_info_settings(callback.from_user.id, callback.data, db_host, db_database, db_user, db_password, db_port))
    )


@router.callback_query(F.data == 'back')
async def process_settings_back(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['/settings'],
        reply_markup=create_settings_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == 'edit_settings')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_edit_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.in_(['edit_games', 'edit_bookies', 'edit_progruz']))
async def process_settings_param(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_kb_edit_params(callback.data, get_info_settings(callback.from_user.id, callback.data.lstrip('edit_'), db_host, db_database, db_user, db_password, db_port))
    )

@router.callback_query(F.data == 'back_edit')
async def process_settings_back(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['edit_settings'],
        reply_markup=create_edit_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.in_(['1x_1', 'fonbet_1', 'cloudbet_1', 'csgopositive_1', 'raybet_1', 'tf_1',
                                   'counter-strike_1', 'dota2_1', 'lol_1', 'valorant_1']))
async def process_settings_param(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await callback.message.edit_reply_markup(reply_markup=edit_kb_edit_params_del(callback))
    edit_params_del(callback.from_user.id, callback.data, db_host, db_database, db_user, db_password, db_port)
    await callback.answer()

@router.callback_query(F.data.in_(['1x_0', 'fonbet_0', 'cloudbet_0', 'csgopositive_0', 'raybet_0', 'tf_0',
                                   'counter-strike_0', 'dota2_0', 'lol_0', 'valorant_0']))
async def process_settings_param(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await callback.message.edit_reply_markup(reply_markup=edit_kb_edit_params_add(callback))
    edit_params_add(callback.from_user.id, callback.data, db_host, db_database, db_user, db_password, db_port)
    await callback.answer()

@router.callback_query(F.data.in_(['0.05_0', '0.1_0', '0.15_0', '0.2_0', '0.25_0', '0.3_0']))
async def process_settings_param(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    await callback.message.edit_reply_markup(reply_markup=edit_kb_edit_params_pro(callback))
    edit_params_pro(callback.from_user.id, callback.data, db_host, db_database, db_user, db_password, db_port)
    await callback.answer()

@router.callback_query(F.data.in_(['1x', 'fonbet', 'cloudbet', 'csgopositive', 'raybet', 'tf',
                                   'counter-strike', 'dota2', 'lol', 'valorant', '0.05_1', '0.1_1', '0.15_1',
                                   '0.05', '0.1', '0.15', '0.2_1', '0.25_1', '0.3_1', '0.2', '0.25', '0.3']))
async def process_settings_param(callback: CallbackQuery):
    await callback.answer()


