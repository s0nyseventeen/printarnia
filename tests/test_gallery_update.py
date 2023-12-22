import io

from src.gallery.models import Image
from src.gallery.models import Work
from src.lib.funcs import get_upload_path


def test_update_work_get_status_code(create_work, client):
    assert client.get('/1/update').status_code == 200


def test_update_work_title(create_work, app, client):
    with app.app_context():
        client.post(
            '/1/update',
            data={'title': 'Updated', 'description': 'Updated design'},
        )
        work = Work.query.get(1)
        assert work.title == 'Updated'
        assert work.description == 'Updated design'


def test_update_work_redirect(create_work, app, client):
    with app.app_context():
        resp = client.post(
            '/1/update', data={'title': 'Test title', 'description': 'Updated'}
        )
    assert resp.headers['Location'] == '/1'


def test_work_image_list(create_work, client):
    assert b'Test title' in client.get('/1/update/images').data


def test_add_work_image_status_code(create_work, client):
    assert client.get('/1/update/images/add_image').status_code == 200


def test_add_work_image_exists_in_db(create_work, app, client):
    with app.app_context():
        client.post(
            '/1/update/images/add_image',
            data={
                'image': (io.BytesIO(b'randomstr'), 'image2.jpg'),
                'image_description': 'Image description'
            },
            content_type='multipart/form-data'
        )
        assert len(Image.query.filter_by(work_id=1).all()) == 2


def test_add_work_image_without_description_exists_in_db(
    create_work, app, client
):
    with app.app_context():
        client.post(
            '/1/update/images/add_image',
            data={'image': (io.BytesIO(b'randomstr'), 'image2.jpg')},
            content_type='multipart/form-data'
        )
        assert len(Image.query.filter_by(work_id=1).all()) == 2


def test_add_work_image_redirect(add_new_image):
    assert add_new_image.headers['Location'] == '/1/update/images'


def test_add_work_image_file_exists(app, add_new_image):
    with app.app_context():
        path = get_upload_path()
    assert 'image2.jpg' in [f.name for f in path.iterdir() if f.is_file()]


def test_add_work_image_without_image(create_work, client):
    assert b'Please add a file' in client.post('/1/update/images/add_image').data


def test_detail_image_status_code(create_work, client):
    assert client.get('/1/update/images/detail/1').status_code == 200


def test_detail_image_without_image(create_work, app, client):
    resp = client.post(
        '/1/update/images/detail/1',
        data={'image_description': 'Updated image description'}
    )
    with app.app_context():
        assert Image.query.get(1).description == 'Updated image description'
    assert resp.headers['Location'] == '/1/update/images'


def test_detail_image_with_image_db(update_image, app):
    with app.app_context():
        assert Image.query.get(1).title == 'image2.jpg'
    assert update_image.headers['Location'] == '/1/update/images'


def test_detail_image_with_image_file(update_image, app):
    with app.app_context():
        path = get_upload_path()
        assert 'image2.jpg' in [f.name for f in path.iterdir() if f.is_file()]
    assert update_image.headers['Location'] == '/1/update/images'
