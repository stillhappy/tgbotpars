from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command

from keyboards.zamki_kb import create_locks_games_keyboard, create_tours_keyboard, create_matches_keyboard, create_params_keyboard, create_locks_all_keyboard, create_locks_keyboard
from bd.tg_pass_bd import get_tours_from_game, get_matches_from_game, get_params_from_game, get_locks_all_from_game, get_full_name_tour
from lexicon.dictsl import d_params_to_en, d_en_to_params, d_games_to_s, d_s_to_games


router = Router()


@router.message(Command(commands='locks'))
async def send_locks_menu(message: Message):
    await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_locks_keyboard()
        )


@router.callback_query(F.data == 'cancel_zam')
async def process_cancel_press_from_locks(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['cancel_zam'])
    await callback.answer()

@router.callback_query(F.data.in_(['live', 'line']))
async def games_locks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'<b>Вы перешли в раздел {callback.data}</b>\nВыберите игру:',
        reply_markup=create_locks_games_keyboard(callback.data)
    )
    await callback.answer()

@router.callback_query(F.data == 'back_cat')
async def process_back_to_live_line(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['/locks'],
        reply_markup=create_locks_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.endswith('_gams'))
async def tours_locks(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    status, game = data[1], data[0]
    if game in d_s_to_games:
        game = d_s_to_games[game]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в игру {game}</b>\nВыберите турнир:',
        reply_markup=create_tours_keyboard(game, status, await get_tours_from_game(game, status, db_host, db_database, db_user, db_password, db_port))
    )
    await callback.answer()

@router.callback_query(F.data.endswith('_gama'))
async def process_back_to_games(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'<b>Вы перешли в раздел {callback.data.split('_')[1]}</b>\nВыберите игру:',
        reply_markup=create_locks_games_keyboard(callback.data.split('_')[1])
    )
    await callback.answer()

@router.callback_query(F.data.endswith('_tor'))
async def matches_locks(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    status, game, tour = data[1], data[0], data[2]
    tour = await get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port)
    game = d_s_to_games[game]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в турнир {tour}</b>\nВыберите матч:',
        reply_markup=create_matches_keyboard(game, status, tour,
                                             await get_matches_from_game(status, game, tour, db_host, db_database,
                                                                   db_user, db_password, db_port))
    )
    await callback.answer()
    # Counter-Strike.live.H2H CS.toar

@router.callback_query(F.data.endswith('_toura'))
async def process_back_to_tours(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    status, game, tour = data[2], data[1], data[3]
    game = d_s_to_games[game]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в игру {game}</b>\nВыберите турнир:',
        reply_markup=create_tours_keyboard(game, status, await get_tours_from_game(game, status, db_host, db_database, db_user, db_password, db_port))
    )
    await callback.answer()

@router.callback_query(F.data.endswith('_mch'))
async def params_lock(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    game, status, tour, match = data[0], data[1], data[2], data[3]
    tour = await get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port)
    game = d_s_to_games[game]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в матч {' - '.join(data[3].split('|'))}</b>\nВыберите маркер:',
        reply_markup=create_params_keyboard(game, status, tour, match,
                                             await get_params_from_game(status, game, tour, match, db_host, db_database, db_user,
                                                                   db_password, db_port))
    )
    await callback.answer()

@router.callback_query(F.data.endswith('_mha'))
async def process_back_to_matches(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    status, game, tour = data[2], data[1], data[3]
    tour = await get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port)
    game = d_s_to_games[game]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в турнир {tour}</b>\nВыберите матч:',
        reply_markup=create_matches_keyboard(game, status, tour,
                                             await get_matches_from_game(status, game, tour, db_host, db_database,
                                                                   db_user, db_password, db_port))
    )
    await callback.answer()
    # cs.live.H2H CS.Blue Gem |Dragon Ri.Map1.prm

@router.callback_query(F.data.endswith('prm'))
async def locks_all(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    status, game, tour, match, param = data[1], data[0], data[2], data[3], data[4]
    tour = await get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port)
    game = d_s_to_games[game]
    param = d_en_to_params[param]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в матч {' - '.join(data[3].split('|'))}</b>\nМаркер: <b>{d_en_to_params[data[4]]}</b>',
        reply_markup=create_locks_all_keyboard(await get_locks_all_from_game(status, game, tour, match, param, db_host, db_database,
                                                                 db_user,
                                                                 db_password, db_port))
    )
    await callback.answer()

@router.callback_query(F.data=='clpls')
async def ans_pust(callback: CallbackQuery):
    await callback.answer()

@router.callback_query(F.data.endswith('pra'))
async def process_back_to_params(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('_')
    game, status, tour, match = data[1], data[2], data[3], data[4]
    tour = await get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port)
    game = d_s_to_games[game]
    # back = f'back.{dict[back_list[1]]}.{back_list[0]}.{back_list[2][:9]}.{back_list[3][:9]}|{back_list[4][:9]}.pra'
    await callback.message.edit_text(
        text=f'<b>Вы перешли в матч {' - '.join(data[4].split('|'))}</b>\nВыберите маркер:',
        reply_markup=create_params_keyboard(game, status, tour, match,
                                            await get_params_from_game(status, game, tour, match, db_host, db_database,
                                                                 db_user,
                                                                 db_password, db_port))
    )
    await callback.answer()