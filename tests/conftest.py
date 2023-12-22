import io
import os
from pathlib import Path

from pytest import fixture
from sqlalchemy import text

from src import create_app
from src.extensions import db


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
    __remove_images(app)


def __remove_images(app):
    for image in 'updated.jpg', 'image.jpg', 'image2.jpg':
        try:
            os.remove(Path(app.config['UPLOAD_FOLDER']) / image)
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


@fixture
def register_and_login_admin(app, auth):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')


@fixture
def create_work(register_and_login_admin, client):
    return client.post(
        '/create',
        data={
            'title': 'Test title',
            'image': (io.BytesIO(b'randomstr'), 'image.jpg')
        },
        content_type='multipart/form-data'
    )


@fixture
def add_new_image(create_work, client):
    return client.post(
        '/1/update/images/add_image',
        data={
            'image': (io.BytesIO(b'randomstr'), 'image2.jpg'),
            'image_description': 'Image description'
        },
        content_type='multipart/form-data'
    )


@fixture
def update_image(create_work, client):
    return client.post(
        '/1/update/images/detail/1',
        data={'image': (io.BytesIO(b'randomstr'), 'image2.jpg')},
        content_type='multipart/form-data'
    )
