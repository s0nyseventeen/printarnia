from src.gallery.models import Work
from src.lib.funcs import get_upload_path


def test_index(app, client):
    assert b'1_Leggitop_title_image.svg' in client.get('/').data


def test_index_without_login(client):
    assert b'\xd0\x9f\xd1\x80\xd0\xbe\xd1\x81\xd1\x82\xd1\x96 \xd1\x82\xd0' \
        b'\xb0 \xd0\xb2\xd0\xb8\xd0\xb3\xd1\x96\xd0\xb4\xd0\xbd\xd1\x96 ' \
        b'\xd1\x80\xd1\x96\xd1\x88\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x8f ' \
        b'\xd0\xb4\xd0\xbb\xd1\x8f \xd0\xb1\xd1\x96\xd0\xb7\xd0\xbd\xd0\xb5' \
        b'\xd1\x81\xd1\x83' in client.get('/').data


def test_index_login(register_and_login_admin, client):
    assert b'Create' in client.get('/').data


def test_detail(create_work, client):
    assert b'Test title' in client.get('/1').data


def test_delete_work_dbrecord(app, create_work, client):
    with app.app_context():
        client.post('/1/delete')
        assert not Work.query.get(1)


def test_delete_redirect(create_work, client):
    assert client.post('/1/delete').headers.get('Location') == '/'


def test_delete_remove_photo(app, create_work, client):
    with app.app_context():
        client.post('/1/delete')
        image = get_upload_path() / 'image.jpg'
    assert not image.exists()


def test_remove_photo_image_column_none(create_work, app, client):
    with app.app_context():
        client.post('/remove_photo/1')
        assert not Work.query.get(1).images


def test_remove_photo_remove_file(app, create_work, client):
    with app.app_context():
        client.post('/remove_photo/1')
        path = get_upload_path()
        assert 'image.jpg' not in [f.name for f in path.iterdir() if f.is_file()]


def test_remove_photo_redirect(app, create_work, client):
    with app.app_context():
        assert client.post('/remove_photo/1').headers['Location'] == \
            '/1/update/images'


def test_get_work_non_exist(register_and_login_admin, client):
    assert client.get('/2').status_code == 404
