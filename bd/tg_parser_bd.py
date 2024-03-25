import asyncpg

async def get_tours_from_game_prs(status, game, bk, db_host, db_database, db_user, db_password, db_port):
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
            FROM pars 
            WHERE game_name = $1 AND status = $2 AND bk_name = $3
            ORDER BY tour_name
        """
        tours_name = await conn.fetch(query, game, status, bk)
        return set([tour['tour_name'][:12] for tour in tours_name])
    finally:
        await conn.close()

async def get_matches_from_prs(status, game, bk, tour, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT DISTINCT concat(team1, '*', team2) as match_name
            FROM pars
            WHERE status = $1 AND game_name = $2 AND bk_name = $3 AND tour_name like $4 || '%'
            ORDER BY match_name
        """
        matches_name = await conn.fetch(query, status, game, bk, tour)
        return [match['match_name'] for match in matches_name]
    finally:
        await conn.close()

async def get_params_from_prs(status, game, bk, tour, team1, team2, db_host, db_database, db_user, db_password, db_port):
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
            FROM pars
            WHERE status = $1 AND game_name = $2 AND bk_name = $3 AND tour_name like $4 || '%' AND team1 like $5 || '%'
            AND team2 like $6 || '%'
            ORDER BY params DESC
        """
        params_name = await conn.fetch(query, status, game, bk, tour, team1, team2)
        return [param['params'] for param in params_name]
    finally:
        await conn.close()

async def get_bet_name_kofs_from_prs(status, game, bk, tour, team1, team2, param, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT bet_name, kofs
            FROM (
                SELECT bet_name, kofs, 
                                    ROW_NUMBER() OVER (PARTITION BY bet_name ORDER BY date_request DESC) AS rn
                FROM pars
                WHERE status = $1 
                AND bk_name = $2 
                AND game_name = $3
                AND tour_name like $4 || '%'
                AND team1 like $5 || '%' 
                AND team2 like $6 || '%'
                AND params = $7
                ) t
            WHERE rn = 1
            ORDER BY bet_name;
        """
        bet_name_and_kofs_names = await conn.fetch(query, status, bk, game, tour, team1, team2, param)
        return [f'{ci['bet_name']}|{ci['kofs']}' for ci in bet_name_and_kofs_names]
    finally:
        await conn.close()

async def get_all_kofs(status, game, bk, tour, team1, team2, param, bet_name, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        query = """
            SELECT kofs, date_request
            FROM pars
            WHERE status = $1 AND game_name = $2 AND bk_name = $3 AND tour_name like $4 || '%' AND team1 like $5 || '%'
            AND team2 like $6 || '%' AND params = $7 AND bet_name = $8
            ORDER BY date_request DESC
        """
        all_cofs = await conn.fetch(query, status, game, bk, tour, team1, team2, param, bet_name)
        return [f'{ci['kofs']}|{ci['date_request']}' for ci in all_cofs]
    finally:
        await conn.close()