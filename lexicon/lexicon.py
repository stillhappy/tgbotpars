LEXICON_RU: dict[str, str] = {
    '/start': '<b>Привет!</b> 👋 \n\n'
              'Добро пожаловать в Radar BOT, '
              'который поможет тебе быть в курсе свежих '
              'коэффициентов от ведущих букмекеров! 📈\n\n'
              'Что умеет этот бот \n'
              '🔹 /help - справка по функционалу\n'
              '🔹 /pass - проверка статуса подписки\n'
              '🔹 /settings - настройка персональной рассылки\n\n'
              'Будь на шаг впереди с нашим ботом! 🚀 Настрой уведомления под себя и'
              'получай актуальную информацию с графиками в удобном формате. 📊',
    '/help': '<b>Привет! Я бот-парсер.</b> Вот, что я умею:\n\n'
             '📊 Парсинг коэффициентов по выбранным букмекерам и играм.\n'
             '⚙️ Настройка рассылки под твои предпочтения.\n\n'
             '<b>Чтобы начать, тебе нужна активная подписка.</b> \n'
             'Узнать её статус можно командой /pass.\n\n'
             'Затем настрой рассылку под себя командой /settings: \n\n'
             '1️⃣ Выбери букмекеров \n'
             '2️⃣ Укажи интересующие игры \n'
             '3️⃣ Задай желаемую разницу коэффициентов \n\n'
             'После этого я буду присылать тебе подходящие варианты, '
             'как только они появятся!',
    '/settings': '<b>Это список ваших настроек:</b>',
    '/pass': ['🚫 К сожалению...,\nУ вас еще нет подписки\n\n'
              'Проблемы с подпиской?\n'
              'Обратитесь к <a href="tg://user?id=461491549">администратору</a>',
              '✅ <b>Поздравляю</b>\n'
              'У вас активная подписка.'],
    '/users': '<b>Список пользователей, а также статус подписки</b>',
    'cancel': 'ВЫЙТИ',
    'cancel_text': '✅ <b>Ваши настройки успешно сохранены</b>',
    'bookies_button': 'Мои букмекеры',
    'bookies': '<b>Список ваших букмекеров</b>',
    'edit_bookies_button': 'Редактировать моих букмекеров',
    'edit_bookies': '<b>Редактируйте ваших букмекеров</b>',
    'games_button': 'Мои игры',
    'games': '<b>Список ваших игр</b>',
    'edit_games_button': 'Редактировать мои игры',
    'edit_games': 'Редактируйте ваши игры',
    'progruz_button': 'Мой прогруз',
    'progruz': '<b>Ваш прогруз</b>',
    'edit_progruz_button': 'Редактировать прогруз',
    'edit_progruz': 'Редактируйте прогруз',
    'edit_settings': '<b>Редактировать настройки профиля</b>',
    'edit_settings_button': '⚙️ РЕДАКТИРОВАТЬ',
    'back_edit': 'НАЗАД',
    'back': 'НАЗАД',
    '1x': '1x',
    'fonbet': 'fonbet',
    'cloudbet': 'cloudbet',
    'csgopositive': 'csgopositive',
    'raybet': 'raybet',
    'tf': 'tf',
    'counter-strike': 'Counter-Strike',
    'dota2': 'Dota 2',
    'lol': 'LoL',
    'valorant': 'Valorant',
    '0.05': '0.05',
    '0.1': '0.1',
    '0.15': '0.15',
    '0.2': '0.2',
    '0.25': '0.25',
    '0.3': '0.3',
    '1x_1': '1x ✅',
    'fonbet_1': 'fonbet ✅',
    'cloudbet_1': 'cloudbet ✅',
    'csgopositive_1': 'csgopositive ✅',
    'raybet_1': 'raybet ✅',
    'tf_1': 'tf ✅',
    'counter-strike_1': 'Counter-Strike ✅',
    'dota2_1': 'Dota 2 ✅',
    'lol_1': 'LoL ✅',
    'valorant_1': 'Valorant ✅',
    '0.05_1': '0.05 ✅',
    '0.1_1': '0.1 ✅',
    '0.15_1': '0.15 ✅',
    '0.2_1': '0.2 ✅',
    '0.25_1': '0.25 ✅',
    '0.3_1': '0.3 ✅',
    '1x_0': '1x',
    'fonbet_0': 'fonbet',
    'cloudbet_0': 'cloudbet',
    'csgopositive_0': 'csgopositive',
    'raybet_0': 'raybet',
    'tf_0': 'tf',
    'counter-strike_0': 'Counter-Strike',
    'dota2_0': 'Dota 2',
    'lol_0': 'LoL',
    'valorant_0': 'Valorant',
    '0.05_0': '0.05',
    '0.1_0': '0.1',
    '0.15_0': '0.15',
    '0.2_0': '0.2',
    '0.25_0': '0.25',
    '0.3_0': '0.3',
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'Справка по парсеру',
    '/settings': 'Настройка профиля',
    '/pass': 'Статус подписки'
}