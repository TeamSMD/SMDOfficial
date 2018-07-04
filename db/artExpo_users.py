import sqlite3
from . import artExpo_transaction_log
from .artExpo_transaction_log import transaction_type


def connect():
    return sqlite3.connect('artExpo_data.db')


def make_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""create table users(username text, password text, display_name text, coins)""")
    conn.commit()
    conn.close()


def add_user(username:str, password:str, display_name:str):
    conn = connect()
    cur = conn.cursor()
    cur.execute('insert into users values (?, ?, ?, 0);', (username, password, display_name))
    conn.commit()
    conn.close()


def check_password(username:str, password:str)->bool:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from users where username = ? and password = ?;', (username, password))
    r = cur.fetchall()
    if r[0][0] == 1:
        conn.close()
        return True
    else:
        conn.close()
        return False


def update_password(username:str, password:str, new_password:str)->bool:
    if check_password(username, password):
        conn = connect()
        cur = conn.cursor()
        cur.execute('update users set password = ? where username = ?;', (new_password, username))
        conn.commit()
        conn.close()
        return True
    else:
        return False


def check_username_availability(username:str)->bool:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select count(*) from users where username = ?;', (username, ))
    r = cur.fetchall()
    if r[0][0] == 0:
        conn.close()
        return True
    else:
        conn.close()
        return False


def list_users()->list:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select * from users;')
    users = cur.fetchall()
    r = []
    for user in users:
        user_info = {'username': user[0], 'display_name': user[2], 'coins': user[3]}
        r.append(user_info)
    conn.close()
    return r


def get_coins(username:str)->int:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select coins from users where username = ?;', (username,))
    coins = cur.fetchall()
    if coins.__len__() != 0 :
        coins = coins[0][0]
        conn.close()
        return coins
    else:
        return -1


def add_coins(username:str, coins:int)->bool:
    origional = get_coins(username)
    if origional != -1:
        conn = connect()
        cur = conn.cursor()
        cur.execute('update users set coins = ? where username = ?;', (origional + coins, username))
        conn.commit()
        conn.close()
        artExpo_transaction_log.new_log(transaction_type.add_value, username, coins)
        return True
    else:
        return False


def use_coins(username:str, coins:int)->bool:
    original = get_coins(username)
    coins = int(coins)
    print('from use_coins: ')
    print('original:' + str(original))
    print('coins:' + str(coins))
    if original >= coins:
        conn = connect()
        cur = conn.cursor()
        cur.execute('update users set coins = ? where username = ?;', (original - coins, username))
        conn.commit()
        artExpo_transaction_log.new_log(transaction_type.used_by_account, username, coins)
        return True
    else:
        return False
