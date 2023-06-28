from pathlib import Path
from tempfile import mkstemp

from basic import create_app
from basic.db import get_db, init_db


def app_factory():
    with open(Path().resolve() / 'tests/data.sql') as f:
        data_sql = f.read()

    db_fake, db_path = mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(data_sql)
    return app, db_fake, db_path


class Auth:
    def __init__(self, client):
        self.__client = client

    def login(self, username='test', password='test'):
        return self.__client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')


def get_logfile() -> str:
    with open('basic.log') as f:
        logfile = f.read()
    return logfile
