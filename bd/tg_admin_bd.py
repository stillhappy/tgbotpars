from datetime import datetime, timedelta
import asyncpg
import logging

logger = logging.getLogger(__name__)

async def get_status_users(db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        pass_users = await conn.fetch(f"SELECT user_id, username, first_name, is_pass FROM tg_users ORDER BY is_pass, username")
        return pass_users
    except Exception as e:
        logger.exception(f"Error in get_status_users: {e}")
    finally:
        await conn.close()

async def get_admin(user_id, db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        adm = await conn.fetchval(f"SELECT is_admin FROM tg_users WHERE user_id = {user_id}")
        return adm
    except Exception as e:
        logger.exception(f"Error in get_admin: {e}")
    finally:
        await conn.close()

async def give_pass(user_id: str, db_host, db_database, db_user, db_password, db_port):
    user_id = user_id.rstrip(':0')
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        start_date = datetime.now() + timedelta(hours=3)
        end_date = start_date + timedelta(days=31)
        start_date = start_date.replace(hour=20, minute=0, second=0)
        end_date = end_date.replace(hour=20, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

        await conn.execute(
            f"UPDATE tg_users SET is_pass = true, date_start_pass = '{start_date}', date_end_pass = '{end_date}' WHERE user_id = {user_id}")
    except Exception as e:
        logger.exception(f"Error in give_pass: {e}")
    finally:
        await conn.close()

async def del_pass(user_id: str, db_host, db_database, db_user, db_password, db_port):
    user_id = user_id.rstrip(':1')
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        await conn.execute(
            f"UPDATE tg_users SET is_pass = false, date_start_pass = null, date_end_pass = null WHERE user_id = {user_id}")
    except Exception as e:
        logger.exception(f"Error in del_pass: {e}")
    finally:
        await conn.close()

async def update_pass(db_host, db_database, db_user, db_password, db_port):
    conn = await asyncpg.connect(
        host=db_host,
        database=db_database,
        user=db_user,
        password=db_password,
        port=db_port
    )
    try:
        await conn.execute(
            "UPDATE tg_users SET is_pass = false, date_start_pass = NULL, description = date_end_pass, date_end_pass = NULL WHERE date_end_pass <= NOW();")
    except Exception as e:
        logger.exception(f"Error in del_pass: {e}")
    finally:
        await conn.close()