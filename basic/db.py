from pathlib import Path
from json import load

from flask import current_app
from flask import g
from psycopg2 import connect

with open(Path() / 'instance/test_config.json') as f:
    __DATA = load(f)

__CONN = connect(
    database=__DATA['dbname'],
    host=__DATA['host'],
    user=__DATA['user'],
    password=__DATA['password'],
    port=__DATA['port']
)


class Db:
    def __init__(self, conn):
        if not conn:
            self.__conn = connect(
                database='sheikhs',
                host='localhost',
                user='postgres',
                password='5247942st',
                port='5432'
            )
        else:
            self.__conn = conn
        self.cur = self.__conn.cursor()

    def run_query(self, query):
        self.cur.execute(query)
        self.__conn.commit()


def get_db():
    conn = __CONN if current_app.config['TESTING'] else None
    if 'db' not in g:
        g.db = Db(conn)
    return g.db
