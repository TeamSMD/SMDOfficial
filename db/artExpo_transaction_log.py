import sqlite3, time
from enum import Enum


def connect():
    return sqlite3.connect('artExpo_data.db')


def make_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""create table transaction_log (datetime integer, type integer, id text, amount integer)""")
    conn.commit()
    conn.close()


def new_log(type, id:str, amount:int):
    """
        log a transaction of coin
    :param type: 1: add value to account/ 2: coins used by account/ 3: work gain coin
    :param id: work id / username
    :param amount: the amount of coins involved
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into transaction_log values (?, ?, ?, ?);", (time.time(), type.value, id, amount))
    conn.commit()
    conn.close()


class transaction_type(Enum):
    add_value = 1
    used_by_account = 2
    work_gain_coin = 3