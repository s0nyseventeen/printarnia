import os
from pathlib import Path

from pytest import fixture
from sqlalchemy import text

from src import create_app
from src.extensions import db

DEFAULT_USER = {'username': 'test', 'password': 'test', 'email': 'test@mail.ua'}


@fixture
def app():
    app = create_app({
        'TESTING': True,
        'UPLOAD_FOLDER': 'src/static/images',
        'SECRET_KEY': 'dev',
        'SQLALCHEMY_DATABASE_URI': os.getenv('TESTS_SHEIKHS')
    })

    with open(Path('tests/schema.sql')) as f, app.app_context():
        db.session.execute(text(f.read()))
        db.session.commit()

    yield app
    __remove_image(app)


def __remove_image(app):
    for image in 'someimage.jpg', 'updated.jpg':
        try:
            path = Path(app.config['UPLOAD_FOLDER'])
            os.remove(path / image)
        except FileNotFoundError:
            pass


@fixture
def client(app):
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self.__client = client

    def login(self, username='test', password='test'):
        return self.__client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')

    def register(self, data):
        return self.__client.post('/auth/register', data=data)


@fixture
def auth(client):
    return AuthActions(client)
