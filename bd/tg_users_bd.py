import psycopg2
from datetime import datetime, timedelta

def get_users(message, db_host, db_database, db_user, db_password, admin_ids, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS tg_users(
            user_id BIGINT,
            username VARCHAR(25),
            first_name VARCHAR(25),
            last_name VARCHAR(25),
            is_admin BOOL,
            is_pass BOOL,
            games TEXT,
            bookies TEXT,
            progruz FLOAT,
            user_register_date date,
            UNIQUE (user_id)
        );
    ''')

    user_id = message.from_user.id
    print(user_id)
    cur.execute(f"SELECT COUNT(*) FROM tg_users WHERE user_id = {user_id}")
    user_exists = cur.fetchone()[0]
    print(user_exists)
    if not user_exists:
        cur.execute(f'''
            SET TIME ZONE 'Europe/Moscow';
            INSERT INTO tg_users (user_id, username, first_name, last_name, is_admin, is_pass, games, bookies, progruz, user_register_date)
            VALUES (
                {user_id},
                '{message.from_user.username}',
                '{message.from_user.first_name}',
                '{message.from_user.last_name}',
                {user_id in admin_ids},
                {user_id in admin_ids},
                '{"counter-strike dota2"}',
                '{"1x raybet cloudbet"}',
                {0.1},
                current_date
            )
        ''')

    cur.close()
    conn.close()

def get_status_pass(message, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    user_id = message.from_user.id
    cur = conn.cursor()
    cur.execute(f"SELECT is_pass FROM tg_users WHERE user_id = {user_id}")
    user_exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return user_exists

def get_info_settings(user_id, col, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    cur = conn.cursor()
    cur.execute(f"SELECT {col} FROM tg_users WHERE user_id = {user_id}")
    text_col = cur.fetchone()[0]
    cur.close()
    conn.close()
    return text_col

def edit_params_del(user_id, old_par: str, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    params = 'games' if old_par.rstrip('_1') in ['counter-strike', 'lol', 'valorant', 'dota2'] else 'bookies'
    cur = conn.cursor()
    cur.execute(f"SELECT {params} FROM tg_users WHERE user_id = {user_id}")
    text_params = cur.fetchone()[0].split(' ')
    text_params.remove(old_par.rstrip('_1'))
    text_params = ' '.join(text_params)
    cur.execute(f"UPDATE tg_users SET {params} = '{text_params}' WHERE user_id = {user_id}")
    cur.close()
    conn.close()

def edit_params_add(user_id, old_par: str, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    params = 'games' if old_par.rstrip('_0') in ['counter-strike', 'lol', 'valorant', 'dota2'] else 'bookies'
    cur = conn.cursor()
    cur.execute(f"SELECT {params} FROM tg_users WHERE user_id = {user_id}")
    text_params = cur.fetchone()[0].split(' ')
    text_params.append(old_par.rstrip('_0'))
    text_params = ' '.join(text_params)
    cur.execute(f"UPDATE tg_users SET {params} = '{text_params}' WHERE user_id = {user_id}")
    cur.close()
    conn.close()

def edit_params_pro(user_id, old_par: str, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"UPDATE tg_users SET progruz = {float(old_par.replace('_0', ''))} WHERE user_id = {user_id}")
    cur.close()
    conn.close()

def get_pass_users_with_settings(db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT user_id, games, bookies, progruz, date_end_pass, username, first_name FROM tg_users WHERE is_pass is true")
    pass_users = cur.fetchall()
    cur.close()
    conn.close()
    return pass_users

