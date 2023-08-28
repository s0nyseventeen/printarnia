import pytest
from psycopg2 import InterfaceError

from .conftest import INSERT_INTO_WORK
from basic.db import get_db


def test_db_same_conn(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_get_close_db_cursor(app):
    with app.app_context():
        db = get_db()
        db.cur.execute('SELECT 1')
        db.cur.close()

        with pytest.raises(InterfaceError) as e:
            db.cur.execute('SELECT 1')
            assert 'cursor already closed' in str(e.value)


def test_run_query(app):
    with app.app_context():
        db = get_db()
        db.run_query(INSERT_INTO_WORK)
        db.cur.execute('SELECT * FROM work')
    assert db.cur.fetchall() is not None
