from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command
from aiogram.types import FSInputFile, InputMediaPhoto
import io

from bd.tg_parser_bd import get_tours_from_game_prs, get_matches_from_prs, get_params_from_prs, get_bet_name_kofs_from_prs, get_all_kofs
from lexicon.dictsl import d_nams_to_s, d_s_to_nams, d_bk_to_s, d_s_to_bs, d_s_to_p, d_p_to_s, create_small_text_from_bet_name
from keyboards.parser_kb import (create_parser_kb, create_parser_games_keyboard, create_parser_bks_keyboard,
                                 create_parser_tours_keyboard, create_parser_matches_keyboard,
                                 create_parser_params_keyboard, create_bn_and_k_keyboard)
from services.nice_kofs import process_strings
from services.graphic import plot_coefficientss
from services.del_papka import clear_folder

router = Router()

@router.message(Command(commands='parser'))
async def send_parser_menu(message: Message):
    await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_parser_kb()
        )

@router.callback_query(F.data == 'cancel|pars')
async def process_cancel_parser(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['cancel_mat'])
    await callback.answer()

@router.callback_query(F.data.in_(['lv', 'ln']))
async def games_parser(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'<b>Вы перешли в раздел {LEXICON_RU[callback.data]}</b>\nВыберите игру🎮:',
        reply_markup=create_parser_games_keyboard(callback.data)
    )
    await callback.answer()

@router.callback_query(F.data == 'back|pars')
async def process_back_to_parser(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['/parser'],
        reply_markup=create_parser_kb()
    )
    await callback.answer()

@router.callback_query(F.data.endswith('|bs'))
async def bks_parser(callback: CallbackQuery):
    game = callback.data.split('|')[1]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в игру {d_s_to_nams[game]}</b>\nВыберите БК🃏:',
        reply_markup=create_parser_bks_keyboard(callback.data)
    )
    await callback.answer()


@router.callback_query(F.data.endswith('|gms'))
async def process_back_to_parser(callback: CallbackQuery):
    ct = callback.data.split('|')[1]
    await callback.message.edit_text(
        text=f'<b>Вы перешли в раздел {LEXICON_RU[ct]}</b>\nВыберите игру🎮:',
        reply_markup=create_parser_games_keyboard(ct)
    )
    await callback.answer()

@router.callback_query(F.data.endswith('|tm'))
async def bks_parser(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    bk = data[2]
    status = data[0]
    game = data[1]
    tours = await get_tours_from_game_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_text(
        text=f'<b>Вы перешли в БК {d_s_to_bs[bk]}</b>\nВыберите турнир🏆:',
        reply_markup=create_parser_tours_keyboard(status, game, bk, tours)
    )
    await callback.answer()
    # lv|cs|tf|tm

@router.callback_query(F.data.endswith('|bk'))
async def process_back_to_parser(callback: CallbackQuery):
    data = callback.data.split('|')
    game = data[1]
    data = '|'.join(data[:2])
    await callback.message.edit_text(
        text=f'<b>Вы перешли в игру {d_s_to_nams[game]}</b>\nВыберите БК🃏:',
        reply_markup=create_parser_bks_keyboard(data)
    )
    await callback.answer()
    # lf|cs|1x|blast|m4

@router.callback_query(F.data.endswith('|m4'))
async def match_parser(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    status = data[0]
    game = data[1]
    bk = data[2]
    tour = data[3]
    matches = await get_matches_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_text(
        text=f'<b>Вы перешли в турнир {tour}</b>\nВыберите матч🎲:',
        reply_markup=create_parser_matches_keyboard(status, game, bk, tour, matches)
    )
    await callback.answer()

@router.callback_query(F.data.endswith('|to'))
async def process_back_to_parser(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    game = data[1]
    status = data[0]
    bk = data[2]
    tours = await get_tours_from_game_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], db_host, db_database,
                                          db_user, db_password, db_port)
    await callback.message.edit_text(
        text=f'<b>Вы перешли в БК {d_s_to_bs[bk]}</b>\nВыберите турнир🏆:',
        reply_markup=create_parser_tours_keyboard(status, game, bk, tours)
    )
    await callback.answer()

# lf|cs|1x|to
# lf|cs|1x|blast|navi*vp|pm

@router.callback_query(F.data.endswith('|pm'))
async def param_parser(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    status = data[0]
    game = data[1]
    bk = data[2]
    tour = data[3]
    team1, team2 = data[4].split('*')
    params = await get_params_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1, team2, db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_text(
        text=f'<b>Вы перешли в матч {team1} - {team2}</b>\nВыберите маркер✏️:',
        reply_markup=create_parser_params_keyboard(status, game, bk, tour, team1, team2, params)
    )
    await callback.answer()

@router.callback_query(F.data.endswith('|m3'))
async def process_back_to_parser(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    game = data[1]
    status = data[0]
    bk = data[2]
    tour = data[3]
    matches = await get_matches_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_text(
        text=f'<b>Вы перешли в турнир {tour}</b>\nВыберите матч🎲:',
        reply_markup=create_parser_matches_keyboard(status, game, bk, tour, matches)
    )
    await callback.answer()
    # lf|cs|1x|blast|navi*vp|1|bn

@router.callback_query(F.data.endswith('|bn'))
async def bet_name_and_kofs_parser(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    status = data[0]
    game = data[1]
    bk = data[2]
    tour = data[3]
    team1, team2 = data[4].split('*')
    param = data[5]
    bet_name_kofs = await get_bet_name_kofs_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1, team2, d_s_to_p[param], db_host, db_database, db_user, db_password, db_port)
    await callback.message.edit_text(
        text=f'<b>Вы перешли в маркер: {d_s_to_p[param]}</b>\nМатч: {team1} - {team2}',
        reply_markup=create_bn_and_k_keyboard(status, game, bk, tour, team1, team2, param, bet_name_kofs)
    )
    await callback.answer()

@router.callback_query(F.data.endswith('|bp'))
async def process_back_to_params(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    status = data[0]
    game = data[1]
    bk = data[2]
    tour = data[3]
    team1, team2 = data[4].split('*')
    params = await get_params_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1, team2, db_host, db_database, db_user, db_password, db_port)
    if callback.message.content_type != 'photo':
        await callback.message.edit_text(
            text=f'<b>Вы перешли в матч {team1} - {team2}</b>\nВыберите маркер✏️:',
            reply_markup=create_parser_params_keyboard(status, game, bk, tour, team1, team2, params)
        )
    else:
        await callback.message.answer(
            text=f'<b>Вы перешли в матч {team1} - {team2}</b>\nВыберите маркер✏️:',
            reply_markup=create_parser_params_keyboard(status, game, bk, tour, team1, team2, params)
        )
        await callback.message.delete()
    await callback.answer()
    # lf|cs|1x|blast|navi*vp|bp

@router.callback_query(F.data.endswith('|hk'))
async def get_full_cofs(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    status = data[0]
    game = data[1]
    bk = data[2]
    tour = data[3]
    team1, team2 = data[4].split('*')
    param = data[5]
    bet_name = data[6]
    bet_name_kofs = await get_bet_name_kofs_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1,
                                                     team2, d_s_to_p[param], db_host, db_database, db_user, db_password,
                                                     db_port)
    all_kofs = await get_all_kofs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1,
                                                     team2, d_s_to_p[param], create_small_text_from_bet_name(bet_name, False), db_host, db_database, db_user, db_password,
                                                     db_port)
    if callback.message.content_type != 'photo':
        await callback.message.edit_text(
            text=f'🕒История коэффициентов\n<b>{team1} - {team2}🎲</b>\n<b>{d_s_to_p[param]} - {create_small_text_from_bet_name(bet_name, False)}📊</b>\n\n'
                 f'{process_strings(all_kofs[::-1])}',
            reply_markup=create_bn_and_k_keyboard(status, game, bk, tour, team1, team2, param, bet_name_kofs)
        )
    else:
        await callback.message.answer(
            text=f'🕒История коэффициентов\n<b>{team1} - {team2}🎲</b>\n<b>{d_s_to_p[param]} - {create_small_text_from_bet_name(bet_name, False)}📊</b>\n\n'
                 f'{process_strings(all_kofs[::-1])}',
            reply_markup=create_bn_and_k_keyboard(status, game, bk, tour, team1, team2, param, bet_name_kofs)
        )
        await callback.message.delete()
    await callback.answer()
    # lv|cs|1x|blast|navi*vp|1|fb|hk

@router.callback_query(F.data.endswith('|gk'))
async def get_full_cofs(callback: CallbackQuery, db_host, db_database, db_user, db_password, db_port):
    data = callback.data.split('|')
    status = data[0]
    game = data[1]
    bk = data[2]
    tour = data[3]
    team1, team2 = data[4].split('*')
    param = data[5]
    bet_name = data[6]
    bet_name_kofs = await get_bet_name_kofs_from_prs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1,
                                                     team2, d_s_to_p[param], db_host, db_database, db_user, db_password,
                                                     db_port)
    all_kofs = await get_all_kofs(LEXICON_RU[status], d_s_to_nams[game], d_s_to_bs[bk], tour, team1,
                                                     team2, d_s_to_p[param], create_small_text_from_bet_name(bet_name, False), db_host, db_database, db_user, db_password,
                                                     db_port)
    kofs = [[kof.split('|')[0], kof.split('|')[1][5:-3]] for kof in all_kofs]
    match = f'{tour}_{team1}_{team2}_{d_s_to_p[param]}_{create_small_text_from_bet_name(bet_name, False)}'
    clear_folder('photosparser')
    photo_path = await plot_coefficientss(kofs[::-1], match, d_s_to_bs[bk], d_s_to_nams[game], 'parser')
    if callback.message.content_type != 'photo':
        await callback.message.answer_photo(
            photo=FSInputFile(photo_path),
            caption=f'📈График\n<b>{team1} - {team2}🎲</b>\n<b>{d_s_to_p[param]} - {create_small_text_from_bet_name(bet_name, False)}📊</b>',
            reply_markup=create_bn_and_k_keyboard(status, game, bk, tour, team1, team2, param, bet_name_kofs)
        )
        await callback.message.delete()
    else:
        file = InputMediaPhoto(media=FSInputFile(photo_path), caption=f'📈График\n<b>{team1} - {team2}🎲</b>\n<b>{d_s_to_p[param]} - {create_small_text_from_bet_name(bet_name, False)}📊</b>')
        await callback.message.edit_media(
            file,
            reply_markup=create_bn_and_k_keyboard(status, game, bk, tour, team1, team2, param, bet_name_kofs)
        )
    await callback.answer()


