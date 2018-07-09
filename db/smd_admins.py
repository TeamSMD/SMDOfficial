import sqlite3


def connect():
    return sqlite3.connect('artExpo_data.db')


def make_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""create table smd_admins(username text,
                                           password text,
                                           display_name text,
                                           login_attempt integer)""")
    conn.commit()
    conn.close()


def new_admin(username: str, password: str, display_name: str):
    conn = connect()
    cur = conn.cursor()
    cur.execute('insert into smd_admins values (?, ?, ?, 0)', (username, password, display_name))
    conn.commit()
    conn.close()


def check_password(username: str, password: str)->bool:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from smd_admins where username = ? and password = ?;', (username, password))
    r = cur.fetchall()
    if r[0][0] != 0:
        conn.close()
        return True
    else:
        conn.close()
        return False


def add_fail_attempt(username: str):
    if not user_exists(username):
        return
    conn = connect()
    cur = conn.cursor()
    cur.execute('select login_attempt from smd_admins where username = ?;', (username, ))
    attempt = cur.fetchall()
    attempt = attempt[0][0]
    cur.execute('update smd_admins set login_attempt = ? where username = ?;', (attempt+1, username))
    conn.commit()
    conn.close()


def clear_fail_attempt(username: str):
    if not user_exists(username):
        return
    conn = connect()
    cur = conn.cursor()
    cur.execute('update smd_admins set login_attempt = 0 where username = ?;', (username, ))
    conn.commit()
    conn.close()


def check_login_attempt(username: str)->bool:
    if not user_exists(username):
        return False
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from smd_admins  where username = ? and login_attempt <= 10;', (username, ))
    r = cur.fetchall()
    if r[0][0] != 0:
        conn.close()
        return True
    else:
        conn.close()
        return False


def update_password(username: str, password: str):
    conn = connect()
    cur = conn.cursor()
    cur.execute('update smd_admins set password = ? where username = ?', (password, username))
    conn.commit()
    conn.close()


def user_exists(username: str)->bool:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from smd_admins where username = ?;', (username, ))
    r = cur.fetchall()
    if r[0][0] == 0:
        return False
    else:
        return True
