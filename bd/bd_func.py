import psycopg2
import json
import datetime
def get_matches(conn):
    cur = conn.cursor()
    cur.execute("SELECT bk_name, game_name, tour_name, team1, team2, params, bet_name FROM pars WHERE status = 'line' GROUP BY bk_name, game_name, tour_name, team1, team2, params, bet_name ORDER BY bk_name")
    matches_info = cur.fetchall()
    cur.close()
    return matches_info

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%m-%d %H:%M")

    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def get_last_kofs(conn, match_info, dict_kofs_matches):
    bk_name_i, game_name_i, tour_name_i, team1_i, team2_i, params_i, bet_name_i = match_info
    cur = conn.cursor()
    query = "SELECT kofs, date_request FROM pars WHERE bk_name=%s AND game_name=%s AND tour_name=%s AND team1=%s AND team2=%s AND params=%s AND bet_name=%s AND status = 'line' ORDER BY date_request"
    cur.execute(query, (bk_name_i, game_name_i, tour_name_i, team1_i, team2_i, params_i, bet_name_i))
    dict_kofs_matches[bk_name_i][game_name_i][f"{tour_name_i}_{team1_i}_{team2_i}_{params_i}_{bet_name_i}"]=dict_kofs_matches[bk_name_i][game_name_i].get(f"{tour_name_i}_{team1_i.replace('_', '-')}_{team2_i.replace('_', '-')}_{params_i}_{bet_name_i}", cur.fetchall())
    cur.close()


def get_json_cofs(host, database, user, password, db_port):
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=db_port
    )
    dict_kofs_matches = {'1x': {'LoL': {}, 'Dota 2': {}, 'Counter-Strike': {}, 'Valorant': {}},
                         'csgopositive': {'LoL': {}, 'Dota 2': {}, 'Counter-Strike': {}, 'Valorant': {}},
                         'Fonbet': {'LoL': {}, 'Dota 2': {}, 'Counter-Strike': {}, 'Valorant': {}},
                         'TF': {'LoL': {}, 'Dota 2': {}, 'Counter-Strike': {}, 'Valorant': {}},
                         'raybet': {'LoL': {}, 'Dota 2': {}, 'Counter-Strike': {}, 'Valorant': {}},
                         'Cloudbet': {'LoL': {}, 'Dota 2': {}, 'Counter-Strike': {}, 'Valorant': {}}}
    with open('output.json', 'w') as file:
        for match_info in get_matches(conn):
            get_last_kofs(conn, match_info, dict_kofs_matches)

        json.dump(dict_kofs_matches, file, default=serialize_datetime, sort_keys=True)


if __name__ == '__main__':
    get_json_cofs()
    
'''
insert into pars (status, bk_name, game_name, tour_name, team1, team2, date_match, params, bet_name, kofs, date_request)
values('line', '1x', 'Counter-Strike', 'angel', 'Boss', 'Nouns', '2024-03-08 01:00:00', '1-я карта', 'Исходы','1.2 4.0', '2024-03-09 00:35:00')
'''