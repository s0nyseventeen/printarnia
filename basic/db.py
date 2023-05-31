from sqlite3 import connect, PARSE_DECLTYPES, Row
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = connect(
            current_app.config['DATABASE'],
            detect_types=PARSE_DECLTYPES
        )
        g.db.row_factory = Row
    return g.db


def __close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def __init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
