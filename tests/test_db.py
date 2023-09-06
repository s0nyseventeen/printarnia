import pytest
import psycopg2

from flask import g

from .conftest import INSERT_INTO_WORK
from basic.db import close_db
from basic.db import get_db
from basic.db import init_app


def test_init_app_close_db(app):
    init_app(app)
    assert 'close_db' in app.teardown_appcontext_funcs[0].__name__


def test_close_db_g_db_is_none(app):
    with app.app_context():
        close_db()
        assert g.pop('db', None) is None


def test_close_db(app):
    with app.app_context():
        db = get_db()

    with pytest.raises(psycopg2.InterfaceError) as e:
        db.cur.execute('SELECT 1')

    assert 'cursor already closed' in str(e.value)


def test_db_conn(app):
    with app.app_context():
        db = get_db()
    assert isinstance(db.conn, psycopg2.extensions.connection)


def test_db_cur(app):
    with app.app_context():
        db = get_db()
    assert isinstance(db.cur, psycopg2.extensions.cursor)


def test_run_query(app):
    with app.app_context():
        db = get_db()
        db.run_query(INSERT_INTO_WORK)
        db.cur.execute('SELECT * FROM work')
        assert db.cur.fetchall() is not None


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
