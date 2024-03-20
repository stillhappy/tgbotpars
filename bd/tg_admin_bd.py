import psycopg2
from datetime import datetime, timedelta

def get_status_users(db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT user_id, username, first_name, is_pass FROM tg_users")
    pass_users = cur.fetchall()
    cur.close()
    conn.close()
    return pass_users

def get_admin(user_id, db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT is_admin FROM tg_users WHERE user_id = {user_id}")
    adm = cur.fetchone()[0]
    cur.close()
    conn.close()
    return adm

def give_pass(user_id: str, db_host, db_database, db_user, db_password, db_port):
    user_id = user_id.rstrip(':0')
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    start_date = datetime.now() + timedelta(hours=3)
    end_date = start_date + timedelta(days=31)
    start_date = start_date.replace(hour=20, minute=0, second=0)
    end_date = end_date.replace(hour=20, minute=0, second=0)
    start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

    cur = conn.cursor()
    cur.execute(f"UPDATE tg_users SET is_pass = true, date_start_pass = '{start_date}', date_end_pass = '{end_date}' WHERE user_id = {user_id}")
    cur.close()
    conn.close()

def del_pass(user_id: str, db_host, db_database, db_user, db_password, db_port):
    user_id = user_id.rstrip(':1')
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"UPDATE tg_users SET is_pass = false, date_start_pass = null, date_end_pass = null WHERE user_id = {user_id}")
    cur.close()
    conn.close()

def update_pass(db_host, db_database, db_user, db_password, db_port):
    conn = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("UPDATE tg_users SET is_pass = false, date_start_pass = NULL, description = date_end_pass, date_end_pass = NULL WHERE date_end_pass <= NOW();")
    cur.close()
    conn.close()