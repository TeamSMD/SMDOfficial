import sqlite3
from . import artExpo_transaction_log
from .artExpo_transaction_log import transaction_type
import json


def connect() -> sqlite3.Connection:
    """
        connect to db
    :return: sqlite3.Connection
    """
    conn = sqlite3.connect('artExpo_data.db')
    return conn


def make_table():
    """
        create table
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""create table 'art_detail' (id integer primary key,
                                              name text,
                                              author integer,
                                              description text,
                                              coins integer)""")
    cur.execute("""create table 'author_detail' (id integer primary key,
                                                  name text,
                                                  description text)""")
    # author_detail:
    # details are stored by json in field description
    # therefore authors may have different information to show
    conn.commit()
    conn.close()


def new_art_work(name:str, author:int, description:str):
    conn = connect()
    cur = conn.cursor()
    cur.execute('insert into art_detail (name, author, description, coins) values (?, ?, ?, 0);', (name,author,description))
    conn.commit()
    conn.close()


def new_author(name:str, description:str):
    """
        add new author
    :param name: name
    :param description: stored by json, dump dict into json first
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('insert into author_detail (name, description) values (?, ?);', (name, description))
    conn.commit()
    conn.close()


def get_coin_count(id:int)->int:
    """
        to know how many coins an art work has
    :param id: the id of the art work
    :return: number of coins if the art work is found, or -1 will be returned
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute('select coins from art_detail where id = ?;', (id, ))
    r = cur.fetchall()
    if r.__len__() != 0:
        coin = int(r[0][0])
        conn.close()
        return coin
    else:
        conn.close()
        return -1


def add_coin(id:int, coin_count:int):
    """
        add coins to an art work
    :param id: the id of the art work
    :param coin_count: the number of coins to add
    """
    origional = get_coin_count(id)
    if origional != -1:
        conn = connect()
        cur = conn.cursor()
        cur.execute('update art_detail set coins = ? where id = ?;', ((origional+coin_count), id))
        conn.commit()
        conn.close()
        artExpo_transaction_log.new_log(transaction_type.work_gain_coin, str(id), coin_count)
    else:
        raise Exception('Art Work Not Found')


def get_work(id:int)->dict:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select * from art_detail where id = ?;', (id,))
    r = cur.fetchall()
    if r.__len__() !=0:
        work_info = {'name': r[0][1], 'author': r[0][2], 'description': r[0][3], 'coins': r[0][4]}
        conn.close()
        return work_info
    else:
        conn.close()
        return {'error': 'Not Found'}


def get_author(id:int)->dict:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select * from author_detail where id = ?;', (id, ))
    r = cur.fetchall()
    if r.__len__() != 0:
        print(r[0][2])
        author_info = {'name': r[0][1], 'description': json.loads(r[0][2])}
        conn.close()
        return author_info
    else:
        conn.close()
        return {'error': 'Not Found'}


def list_all_works()->list:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select * from art_detail;')
    works = cur.fetchall()
    r = []
    for w in works:
        work_info = {'name': w[1], 'author': w[2], 'description': w[3], 'coins': w[4]}
        r.append(work_info)
    conn.close()
    return r


def list_all_author()->list:
    conn = connect()
    cur = conn.cursor()
    cur.execute('select * from author_detail;')
    authors = cur.fetchall()
    r = []
    for a in authors:
        author_info = {'name': a[1], 'description': a[2]}
        r.append(author_info)
    conn.close()
    return r
