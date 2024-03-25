from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

def create_locks_keyboard():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Live',
            callback_data='live'
        ),
        InlineKeyboardButton(
            text='Line',
            callback_data='line'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel_mat'
        ),
        width=1
    )
    return kb_builder.as_markup()

def create_locks_games_keyboard(data):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Counter-Strike',
            callback_data=f'Counter-Strike_{data}_gams'
        ),
        InlineKeyboardButton(
            text='Dota 2',
            callback_data=f'Dota 2_{data}_gams'
        ),
        InlineKeyboardButton(
            text='LoL',
            callback_data=f'LoL_{data}_gams'
        ),
        InlineKeyboardButton(
            text='Valorant',
            callback_data=f'Valorant_{data}_gams'
        ),

        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data='back_cat'
        ),
        width=1
    )
    return kb_builder.as_markup()

def create_tours_keyboard(game, status, tours):
    kb_builder = InlineKeyboardBuilder()
    dict = {'Counter-Strike': 'cs', 'Dota 2': 'd2', 'Valorant': 'vl', 'LoL': 'LoL'}
    for tour in tours:
        kb_builder.row(
            InlineKeyboardButton(
                text=tour,
                callback_data=f"{dict[game]}_{status}_{tour[:9]}_tor"
                # Counter-Strike.live.H2H CS.toar
            ))
    kb_builder.row(
            InlineKeyboardButton(
                text=LEXICON_RU['back'],
                callback_data=f'back_{status}_gama'
            )
        )
    return kb_builder.as_markup()

def create_matches_keyboard(game, status, tour, matches):
    kb_builder = InlineKeyboardBuilder()
    # Counter-Strike.live.H2H CS.toar
    dict = {'Counter-Strike': 'cs', 'Dota 2': 'd2', 'Valorant': 'vl', 'LoL': 'LoL'}
    for match in matches:
        kb_builder.row(
            InlineKeyboardButton(
                text=match,
                callback_data=f"{dict[game]}_{status}_{tour[:9]}_{match}_mch"
                # Counter-Strike.live.H2H CS.Dragon Riders | team2.mch
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'back_{dict[game]}_{status}_{tour[:9]}_toura'
            # back.Counter-Strike.live.H2H CS.toura
        )
    )
    return kb_builder.as_markup()


def create_params_keyboard(game, status, tour, match, params):
    kb_builder = InlineKeyboardBuilder()
    dict = {'Counter-Strike': 'cs', 'Dota 2': 'd2', 'Valorant': 'vl', 'LoL': 'LoL'}
    d_en_to_params = {'Gen': 'Общая', 'Map1': '1-я карта', 'Map2': '2-я карта', 'Map3': '3-я карта',
                      'Map4': '4-я карта', 'Map5': '5-я карта'}
    team1, team2 = match.split('|')
    for param in params:
        kb_builder.row(
            InlineKeyboardButton(
                text=d_en_to_params[param],
                callback_data=f'{dict[game]}_{status}_{tour[:9]}_{team1[:9]}|{team2[:9]}_{param}_prm'
            )
        )
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'back_{dict[game]}_{status}_{tour[:9]}_mha'
        )
    )
    return kb_builder.as_markup()

def create_locks_all_keyboard(all_match_info):
    dict = {'Counter-Strike': 'cs', 'Dota 2': 'd2', 'Valorant': 'vl', 'LoL': 'LoL'}
    back_list = all_match_info[0]
    kb_builder = InlineKeyboardBuilder()
    back = f'back_{dict[back_list[1]]}_{back_list[0]}_{back_list[2][:9]}_{back_list[3][:9]}|{back_list[4][:9]}_pra'
    for lock in all_match_info:
        bet_name, blocks1, blocks2 = lock[6], lock[8], lock[9]
        if 'Исходы' in bet_name:
            txt = f'П1 ➡️ {blocks1} | {bet_name} | {blocks2} ⬅️ П2'
        elif 'Фора' in bet_name:
            if '-' in bet_name:
                txt = f'{bet_name.lstrip('Фора 1 ').replace("(", "").replace(")", "")} ➡️ {blocks1} | {bet_name} | {blocks2} ⬅️ {bet_name.lstrip('Фора 1 ').replace("(", "").replace(")", "").replace("-", "+")}'
            else:
                txt = f'{bet_name.lstrip('Фора 1 ').replace("(", "").replace(")", "")} ➡️ {blocks1} | {bet_name} | {blocks2} ⬅️ {bet_name.lstrip('Фора 1 ').replace("(", "").replace(")", "").replace("+", "-")}'
        elif 'Тотал' in bet_name:
            txt = f'{bet_name.lstrip('Тотал ').replace("(", "").replace(")", "")} ➡️ {blocks1} | {bet_name} | {blocks2} ⬅️ {bet_name.lstrip('Тотал ').replace("(", "").replace(")", "").replace("Б", "М")}'
        else:
            txt = f'{blocks1} | {bet_name} | {blocks2}'
        kb_builder.row(
            InlineKeyboardButton(
                text=txt,
                callback_data='clpls'
            )
        )
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=back
        )
    )
    return kb_builder.as_markup()