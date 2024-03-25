from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_RU
from lexicon.dictsl import d_nams_to_s, d_bk_to_s, d_s_to_nams, d_s_to_bs, d_p_to_s, d_s_to_p, create_small_text_from_bet_name

def create_parser_kb():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Live',
            callback_data='lv'
        ),
        InlineKeyboardButton(
            text='Line',
            callback_data='ln'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel|pars'
        ),
        width=1
    )
    return kb_builder.as_markup()

def create_parser_games_keyboard(data):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Counter-Strike',
            callback_data=f'{data}|cs|bs'
        ),
        InlineKeyboardButton(
            text='Dota 2',
            callback_data=f'{data}|d2|bs'
        ),
        InlineKeyboardButton(
            text='LoL',
            callback_data=f'{data}|ll|bs'
        ),
        InlineKeyboardButton(
            text='Valorant',
            callback_data=f'{data}|vl|bs'
        ),

        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data='back|pars'
        ),
        width=1
    )
    return kb_builder.as_markup()

def create_parser_bks_keyboard(data):
    kb_builder = InlineKeyboardBuilder()
    data = '|'.join(data.split('|')[:2])
    kb_builder.row(
        InlineKeyboardButton(
            text='1x',
            callback_data=f'{data}|1x|tm'
        ),
        InlineKeyboardButton(
            text='csgopositive',
            callback_data=f'{data}|pz|tm'
        ),
        InlineKeyboardButton(
            text='Cloudbet',
            callback_data=f'{data}|cb|tm'
        ),
        InlineKeyboardButton(
            text='Fonbet',
            callback_data=f'{data}|fb|tm'
        ),
        InlineKeyboardButton(
            text='TF',
            callback_data=f'{data}|tf|tm'
        ),
        InlineKeyboardButton(
            text='Raybet',
            callback_data=f'{data}|rb|tm'
        ),

        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'back|{data}|gms'
        ),
        width=1
    )
    return kb_builder.as_markup()

def create_parser_tours_keyboard(status, game, bk, tours):
    kb_builder = InlineKeyboardBuilder()
    for tour in tours:
        kb_builder.row(
            InlineKeyboardButton(
                text=tour,
                callback_data=f"{status}|{game}|{bk}|{tour[:12]}|m4"
                # lf|cs|1x|blast|m4
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'{status}|{game}|bk'
        )
    )
    return kb_builder.as_markup()

def create_parser_matches_keyboard(status: str, game: str, bk: str, tour: str, matches):
    kb_builder = InlineKeyboardBuilder()
    for match in matches:
        team1, team2 = match.split('*')
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{team1} - {team2}',
                callback_data=f"{status}|{game}|{bk}|{tour[:12]}|{team1[:9]}*{team2[:9]}|pm"
                # lf|cs|1x|blast|navi*vp|pm
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'{status}|{game}|{bk}|to'
        )
    )
    return kb_builder.as_markup()

def create_parser_params_keyboard(status, game, bk, tour, team1, team2, params):
    kb_builder = InlineKeyboardBuilder()
    for param in params:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{param}',
                callback_data=f"{status}|{game}|{bk}|{tour[:12]}|{team1[:9]}*{team2[:9]}|{d_p_to_s[param]}|bn"
                # lf|cs|1x|blast|navi*vp|1|bn
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'{status}|{game}|{bk}|{tour[:12]}|m3'
        )
    )
    return kb_builder.as_markup()

def create_bn_and_k_keyboard(status, game, bk, tour, team1, team2, param, data):
    kb_builder = InlineKeyboardBuilder()
    for dat in data:
        bet_name, kofs = dat.split('|')
        kof1, kof2 = kofs.split(' ')
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{kof1} {bet_name} {kof2}',
                callback_data=f"{team1}|{team2}|{bet_name}|kl"
            ))
        kb_builder.row(
            InlineKeyboardButton(
                text='🕒',
                callback_data=f"{status}|{game}|{bk}|{tour}|{team1}*{team2}|{param}|{create_small_text_from_bet_name(bet_name)}|hk"
            ),
            InlineKeyboardButton(
                text='📈',
                callback_data=f"{status}|{game}|{bk}|{tour}|{team1}*{team2}|{param}|{create_small_text_from_bet_name(bet_name)}|gk"
            ),
            width=2
        )
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data=f'{status}|{game}|{bk}|{tour}|{team1}*{team2}|bp'
        )
    )
    return kb_builder.as_markup()