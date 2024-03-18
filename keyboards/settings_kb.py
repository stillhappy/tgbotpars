from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

def create_users_keyboard(users: list):
    kb_builder = InlineKeyboardBuilder()
    for user in users:
        user_info = f'@{user[1]} - {user[2]} {"✅" if user[3] else "🚫"}'
        kb_builder.row(InlineKeyboardButton(
            text=user_info,
            callback_data=f'{user[0]}:{1 if user[3] else 0}'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel'
        ))
    return kb_builder.as_markup()

def create_settings_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    buttons = ['bookies_button', 'games_button', 'progruz_button']
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    for button in buttons:
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON_RU[f'{button}'],
            callback_data=f'{button.replace('_button', '')}'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['edit_settings_button'],
            callback_data='edit_settings'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['cancel'],
            callback_data='cancel'
        ),
        width=2
    )
    return kb_builder.as_markup()

def create_edit_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    buttons = ['edit_bookies_button', 'edit_games_button', 'edit_progruz_button']
    for button in buttons:
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON_RU[f'{button}'],
            callback_data=f'{button.replace('_button', '')}'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data='back'
        )
    )
    return kb_builder.as_markup()

def create_kb_params(params: str):
    kb_builder = InlineKeyboardBuilder()
    for but in str(params).split(' '):
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON_RU[f'{but}'],
            callback_data=but
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back'],
            callback_data='back'
        )
    )
    return kb_builder.as_markup()

def create_kb_edit_params(button: str, params: str):
    dict_settings = {'edit_games': ['counter-strike', 'dota2', 'valorant', 'lol'],
                     'edit_bookies': ['1x', 'csgopositive', 'raybet', 'fonbet', 'tf', 'cloudbet'],
                     'edit_progruz': ['0.05', '0.1', '0.15', '0.2', '0.25', '0.3']}
    kb_builder = InlineKeyboardBuilder()
    for but in dict_settings[button]:
        if but in str(params):
            kb_builder.row(InlineKeyboardButton(
                text=LEXICON_RU[f'{but}_1'],
                callback_data=f'{but}_1'
            ))
        else:
            kb_builder.row(InlineKeyboardButton(
                text=LEXICON_RU[f'{but}_0'],
                callback_data=f'{but}_0'
            ))

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['back_edit'],
            callback_data='back_edit'
        )
    )
    return kb_builder.as_markup()

def edit_kb_edit_params_del(callback):
    reply_markup = callback.message.reply_markup
    for row in reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                button.text = LEXICON_RU[callback.data.replace('_1', '_0')]
                button.callback_data = callback.data.replace('_1', '_0')
                break
    return reply_markup

def edit_kb_edit_params_add(callback):
    reply_markup = callback.message.reply_markup
    for row in reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                button.text = LEXICON_RU[callback.data.replace('_0', '_1')]
                button.callback_data = callback.data.replace('_0', '_1')
                break
    return reply_markup

def edit_kb_edit_params_pro(callback):
    reply_markup = callback.message.reply_markup
    for row in reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data and '_0' in button.callback_data:
                button.text = LEXICON_RU[callback.data.replace('_0', '_1')]
                button.callback_data = callback.data.replace('_0', '_1')
            elif '_1' in button.callback_data and button.callback_data != callback.data:
                button.text = LEXICON_RU[button.callback_data.replace('_1', '_0')]
                button.callback_data = button.callback_data.replace('_1', '_0')
    return reply_markup