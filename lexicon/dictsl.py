d_params_to_en = {'Общая': 'Gen', '1-я карта': 'Map1', '2-я карта': 'Map2', '3-я карта': 'Map3', '4-я карта': 'Map4', '5-я карта': 'Map5'}
d_en_to_params = {'Gen': 'Общая', 'Map1': '1-я карта', 'Map2': '2-я карта', 'Map3': '3-я карта', 'Map4': '4-я карта', 'Map5': '5-я карта'}
d_games_to_s = {'Counter-Strike': 'cs', 'Dota 2': 'd2', 'Valorant': 'vl', 'LoL': 'LoL'}
d_s_to_games = {'cs': 'Counter-Strike', 'd2': 'Dota 2', 'vl': 'Valorant', 'LoL': 'LoL'}
d_nams_to_s = {'Counter-Strike': 'cs', 'Dota 2': 'd2', 'Valorant': 'vl', 'LoL': 'll'}
d_s_to_nams = {'cs': 'Counter-Strike', 'd2': 'Dota 2', 'vl': 'Valorant', 'll': 'LoL'}
d_bk_to_s = {'1x': '1x', 'csgopositive': 'pz', 'Cloudbet': 'cb', 'Fonbet': 'fb', 'TF': 'tf', 'raybet': 'rb'}
d_s_to_bs = {'1x': '1x', 'pz': 'csgopositive', 'cb': 'Cloudbet', 'fb': 'Fonbet', 'tf': 'TF', 'rb': 'raybet'}
d_p_to_s = {'1-я карта': '1', '2-я карта': '2', '3-я карта': '3', '4-я карта': '4', '5-я карта': '5', 'Общая': '0'}
d_s_to_p = {'1': '1-я карта', '2': '2-я карта', '3': '3-я карта', '4': '4-я карта', '5': '5-я карта', '0': 'Общая'}

def create_small_text_from_bet_name(bet_name, to_small=True):
    dict_from_s_to_full = {'wn': 'Исходы', 'oek': 'Тотал Киллов (Odd/Even)', 'oer': 'Тотал Раундов (Odd/Even)',
                           'p1': '1-й Пистолетный раунд', 'p2': '2-й Пистолетный раунд', 'fb': 'Первая кровь'}
    if to_small:
        if '(Odd/Even)' in bet_name:
            if 'Киллов' in bet_name:
                return 'oek'
            else:
                return 'oer'
        elif 'Пистолетный раунд' in bet_name:
            return f'p{bet_name[0]}'
        elif 'Гонка' in bet_name:
            return f'g{bet_name.lstrip('Гонка до ').rstrip(' киллов')}'
        elif 'Исходы' in bet_name:
            return 'wn'
        elif 'Первая кровь' in bet_name:
            return 'fb'
        elif 'Тотал' in bet_name:
            if 'Б':
                'Гонка до 15 киллов'
                return f'tb{bet_name.lstrip('Тотал Б (').rstrip(')')}'
            return f't{bet_name.lstrip('Тотал Б (').rstrip(')')}'
        else:
            if 'Фора 1' in bet_name:
                return f'fr{bet_name.lstrip('Фора 1 (').rstrip(')')}'
            return f'f{bet_name.lstrip('Фора 1 (').rstrip(')')}'
    else:
        if bet_name in dict_from_s_to_full:
            return dict_from_s_to_full[bet_name]
        elif 'g' in bet_name:
            return f'Гонка до {bet_name[1:]} киллов'
        elif 't' in bet_name:
            if 'b' in bet_name:
                return f'Тотал Б ({bet_name[2:]})'
            else:
                return f'Тотал ({bet_name[1:]})'
        else:
            if 'r' in bet_name:
                return f'Фора 1 ({bet_name[2:]})'
            else:
                return f'Фора ({bet_name[1:]})'

# testlist = ['Исходы', 'Тотал Б (12.5)', 'Фора (+2.5)', 'Первая кровь', '1-й Пистолетный раунд', 'Тотал Киллов (Odd/Even)', 'Гонка до 15 киллов']
# for test in testlist:
#     print(test, create_small_text_from_bet_name(test), create_small_text_from_bet_name(create_small_text_from_bet_name(test), False))
