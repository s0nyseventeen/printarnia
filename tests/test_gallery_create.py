import io

from src.gallery.models import Work
from src.lib.funcs import get_upload_path


def test_create_get_status_code(register_and_login_admin, client):
    assert client.get('/create').status_code == 200


def test_create_without_title_flash(register_and_login_admin, client):
    resp = client.post(
        '/create',
        data={'title': '', 'image': (io.BytesIO(b'randomstr'), 'image.jpg')},
        content_type='multipart/form-data'
    )
    assert b'Title is required' in resp.data


def test_create_without_image_db(app, client, register_and_login_admin):
    with app.app_context():
        client.post(
            '/create',
            data={
                'title': 'Test title',
                'image': (io.BytesIO(b'randomstr'), '')
            },
            content_type='multipart/form-data'
        )
        assert not Work.query.get(1).images


def test_create_without_image_redirect(create_work):
    assert create_work.headers['Location'] == '/'


def test_create_with_image_check_if_image_exists_in_db(app, create_work):
    with app.app_context():
        assert Work.query.get(1).images[0].title == 'image.jpg'


def test_create_with_image_redirect(create_work):
    assert create_work.headers['Location'] == '/'


def test_create_with_image_static_file(app, create_work):
    with app.app_context():
        path = get_upload_path()
        assert 'image.jpg' in [f.name for f in path.iterdir() if f.is_file()]
