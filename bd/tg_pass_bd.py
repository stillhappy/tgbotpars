import psycopg2

def get_pass(user_id, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT is_pass FROM tg_users WHERE user_id = {user_id}")
    pss = cur.fetchone()[0]
    cur.close()
    conn.close()
    return pss

def get_tours_from_game(game, status, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT tour_name FROM zamki WHERE game_name='{game}' AND status='{status}' ORDER BY tour_name")
    tours_name = cur.fetchall()
    cur.close()
    conn.close()
    return tours_name

def get_matches_from_game(status, game, tour, db_host, db_database, db_user, db_password, db_port):
    # Counter-Strike.live.H2H CS.toar
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT concat(team1, '|', team2) as match_name from zamki WHERE status='{status}' AND game_name='{game}' AND tour_name like '{tour}%' ORDER BY match_name")
    matches_name = cur.fetchall()
    cur.close()
    conn.close()
    return matches_name

def get_params_from_game(status, game, tour, match, db_host, db_database, db_user,
                                                                   db_password, db_port):
    team1, team2 = match.split('|')
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    dict = {'Общая': 'Gen', '1-я карта': 'Map1', '2-я карта': 'Map2', '3-я карта': 'Map3', '4-я карта': 'Map4', '5-я карта': 'Map5'}
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT params FROM zamki WHERE status='{status}' AND game_name='{game}' AND tour_name like '{tour}%' AND team1 like '{team1}%' AND team2 like '{team2}%' ORDER BY params")
    params_names = cur.fetchall()
    params_names = [dict[ci[0]] for ci in params_names]
    cur.close()
    conn.close()
    return params_names

def get_locks_all_from_game(status, game, tour, match, param, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    team1, team2 = match.split('|')
    cur = conn.cursor()
    cur.execute(f"SELECT status, game_name, tour_name, team1, team2, params, bet_name, blocks, n1_blocks, n2_blocks FROM zamki "
                f"WHERE status='{status}' AND game_name='{game}' AND tour_name like '{tour}%' AND team1 like '{team1}%'"
                f"AND team2 like '{team2}%' AND params='{param}'"
                f"ORDER BY bet_name")
    all_locks_info = cur.fetchall()
    cur.close()
    conn.close()
    return all_locks_info

def get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port ):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    cur = conn.cursor()
    cur.execute(F"SELECT DISTINCT tour_name FROM zamki WHERE tour_name like '{tour}%' LIMIT 1")
    full_name_tour = cur.fetchone()[0]
    cur.close()
    conn.close()
    return full_name_tour