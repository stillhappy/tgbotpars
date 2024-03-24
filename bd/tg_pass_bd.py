import asyncpg


async def get_pass(user_id, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        # Выполнение запроса к базе данных для проверки подписки пользователя
        result = await conn.fetchval('SELECT is_pass FROM tg_users WHERE user_id = $1', user_id)
        return result
    finally:
        await conn.close()

async def get_tours_from_game(game, status, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT DISTINCT tour_name 
            FROM zamki 
            WHERE game_name = $1 AND status = $2
            ORDER BY tour_name
        """
        tours_name = await conn.fetch(query, game, status)
        return [tour['tour_name'] for tour in tours_name]
    finally:
        await conn.close()

async def get_matches_from_game(status, game, tour, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT DISTINCT concat(team1, '|', team2) as match_name
            FROM zamki
            WHERE status = $1 AND game_name = $2 AND tour_name LIKE $3 || '%'
            ORDER BY match_name
        """
        matches_name = await conn.fetch(query, status, game, tour)
        return [match['match_name'] for match in matches_name]
    finally:
        await conn.close()

async def get_params_from_game(status, game, tour, match, db_host, db_database, db_user, db_password, db_port):
    team1, team2 = match.split('|')
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT DISTINCT params
            FROM zamki
            WHERE status = $1 AND game_name = $2 AND tour_name LIKE $3 || '%' 
                AND team1 LIKE $4 || '%' AND team2 LIKE $5 || '%'
            ORDER BY params
        """
        params_names = await conn.fetch(query, status, game, tour, team1, team2)
        dict = {'Общая': 'Gen', '1-я карта': 'Map1', '2-я карта': 'Map2', '3-я карта': 'Map3', '4-я карта': 'Map4', '5-я карта': 'Map5'}
        return [dict[param['params']] for param in params_names]
    finally:
        await conn.close()

async def get_locks_all_from_game(status, game, tour, match, param, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        team1, team2 = match.split('|')
        query = """
            SELECT status, game_name, tour_name, team1, team2, params, bet_name, blocks, n1_blocks, n2_blocks
            FROM zamki
            WHERE status = $1 AND game_name = $2 AND tour_name LIKE $3 || '%'
                AND team1 LIKE $4 || '%' AND team2 LIKE $5 || '%' AND params = $6
            ORDER BY bet_name
        """
        all_locks_info = await conn.fetch(query, status, game, tour, team1, team2, param)
        return all_locks_info
    finally:
        await conn.close()

async def get_full_name_tour(tour, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT DISTINCT tour_name
            FROM zamki
            WHERE tour_name LIKE $1 || '%'
            LIMIT 1
        """
        full_name_tour = await conn.fetchval(query, tour)
        return full_name_tour
    finally:
        await conn.close()