from flask import g
from psycopg2 import connect


class Db:
    def __init__(self, conn=None):
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
    if 'db' not in g:
        g.db = Db()
    return g.db
