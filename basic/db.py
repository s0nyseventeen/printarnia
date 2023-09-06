from flask import current_app
from flask import g
from psycopg2 import connect


def init_app(app):
    app.teardown_appcontext(close_db)


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.cur.close()
        db.conn.close()


class Db:
    def __init__(self, conn):
        self.conn = connect(conn)
        self.cur = self.conn.cursor()

    def run_query(self, query):
        self.cur.execute(query)
        self.conn.commit()


def get_db():
    if 'db' not in g:
        g.db = Db(current_app.config['DB'])
    return g.db
