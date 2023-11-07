import io
import os
from pathlib import Path

from canoe.db import get_db
from canoe.gallery import check_image
from canoe.gallery import get_work


def test_index(app, client):
    assert b'1_Leggitop_title_image.svg' in client.get('/').data


def test_index_without_login(client):
    assert b'\xd0\x9f\xd1\x80\xd0\xbe\xd1\x81\xd1\x82\xd1\x96 \xd1\x82\xd0' \
        b'\xb0 \xd0\xb2\xd0\xb8\xd0\xb3\xd1\x96\xd0\xb4\xd0\xbd\xd1\x96 ' \
        b'\xd1\x80\xd1\x96\xd1\x88\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x8f ' \
        b'\xd0\xb4\xd0\xbb\xd1\x8f \xd0\xb1\xd1\x96\xd0\xb7\xd0\xbd\xd0\xb5' \
        b'\xd1\x81\xd1\x83' in client.get('/').data


def test_index_login(auth, client):
    auth.register({
        'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'
    })
    auth.login('admin', 'admin')
    assert b'Create' in client.get('/').data


def test_create_get_status_code(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
    assert client.get('/create').status_code == 200


def test_create_without_title_flash(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        resp = client.post(
            '/create',
            data={
                'title': '',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )
    assert b'Title is required' in resp.data


def test_create_with_image_check_if_image_exists_in_db(
    app, auth, client
):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/create',
            data={
                'title': 'Test title2',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )

        db = get_db()
        db.cur.execute('SELECT * FROM work WHERE id = 2')
        assert db.cur.fetchone()[4] == 'someimage.jpg'


def test_create_with_image_redirect(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        resp = client.post(
            '/create',
            data={
                'title': 'Test title2',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )
    assert resp.headers['Location'] == '/'


def test_create_with_image_static_file(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/create',
            data={
                'title': 'Test title2',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )
    assert 'someimage.jpg' in os.listdir(Path(app.config['UPLOAD_FOLDER']))


def test_create_without_image_db(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/create',
            data={
                'title': 'Test title2',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), '')
            },
            content_type='multipart/form-data'
        )
        db = get_db()
        db.cur.execute('SELECT * FROM work WHERE id = 2')
        assert db.cur.fetchone()[4] is None


def test_create_without_image_redirect(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        resp = client.post(
            '/create',
            data={
                'title': 'Test title2',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), '')
            },
            content_type='multipart/form-data'
        )
    assert resp.headers['Location'] == '/'


def test_update_get_status_code(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
    assert client.get('/1/update').status_code == 200


def test_update_title(app, auth, client):
    with app.app_context():
        db = get_db()
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/1/update',
            data={
                'title': 'Updated',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )

        db = get_db()
        db.cur.execute('SELECT * FROM work WHERE id = 1')
        assert db.cur.fetchone()[1] == 'Updated'


def test_update_description(app, auth, client):
    with app.app_context():
        db = get_db()
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/1/update',
            data={
                'title': 'Test title',
                'description': 'Updated',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )

        db = get_db()
        db.cur.execute('SELECT * FROM work WHERE id = 1')
        assert db.cur.fetchone()[3] == 'Updated'


def test_update_without_image_redirect(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        resp = client.post(
            '/1/update',
            data={
                'title': 'Test title',
                'description': 'Updated',
                'image': (io.BytesIO(b'randomstr'), 'someimage.jpg')
            },
            content_type='multipart/form-data'
        )
    assert resp.headers['Location'] == '/1'


def test_update_with_image_dbrecord(app, auth, client):
    with app.app_context():
        db = get_db()
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/1/update',
            data={
                'title': 'Test title',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'updated.jpg')
            },
            content_type='multipart/form-data'
        )

        db = get_db()
        db.cur.execute('SELECT * FROM work WHERE id = 1')
        assert db.cur.fetchone()[4] == 'updated.jpg'


def test_update_with_image_static_file(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post(
            '/1/update',
            data={
                'title': 'Test title',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'updated.jpg')
            },
            content_type='multipart/form-data'
        )
    assert 'updated.jpg' in os.listdir(Path(app.config['UPLOAD_FOLDER']))


def test_update_with_image_redirect(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        resp = client.post(
            '/1/update',
            data={
                'title': 'Test title',
                'description': 'New design',
                'image': (io.BytesIO(b'randomstr'), 'updated.jpg')
            },
            content_type='multipart/form-data'
        )
    assert resp.headers['Location'] == '/1'


def test_detail(app, client):
    assert b'Test title' in client.get('/1').data


def test_delete_work_dbrecord(app, auth, client):
    with app.app_context():
        db = get_db()
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
        client.post('/1/delete')
        db = get_db()
        db.cur.execute('SELECT * FROM work WHERE id = 1')
        assert db.cur.fetchone() is None


def test_delete_redirect(app, auth, client):
    with app.app_context():
        auth.register(
            {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
        )
        auth.login('admin', 'admin')
    assert client.post('/1/delete').headers.get('Location') == '/'


def test_remove_photo_image_column_none(app, client):
    with (
        app.app_context(),
        open(Path(app.config['UPLOAD_FOLDER']) / 'someimage.jpg', 'wb') as f
    ):
        db = get_db()
        f.write(b'0xbb')
        client.post('/1/remove_photo')
        db.cur.execute('SELECT * FROM work;')
        assert db.cur.fetchone()[4] is None


def test_remove_photo_remove_file(app, client):
    path = Path(app.config['UPLOAD_FOLDER'])
    image = path / 'someimage.jpg'

    with app.app_context(), open(image, 'wb') as f:
        f.write(b'0xbb')
        client.post('/1/remove_photo')
    assert image not in os.listdir(path)


def test_remove_photo_redirect(app, client):
    with (
        app.app_context(),
        open(Path(app.config['UPLOAD_FOLDER']) / 'someimage.jpg', 'wb') as f
    ):
        f.write(b'0xbb')
    assert client.post('/1/remove_photo').headers['Location'] == '/'


def test_get_work_exist(app):
    with app.app_context():
        assert get_work(1)[1] == 'Test title'


def test_get_work_non_exist(auth, client):
    client.post(
        '/auth/register',
        data={'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
    )
    auth.login('admin', 'admin')
    assert client.get('/2/update').status_code == 404


class Image:
    def __init__(self, filename: str = ''):
        self.filename = filename


def test_check_image_true():
    assert check_image(Image())


def test_check_image_false():
    assert not check_image(Image('kit'))
