import io
import os
from pathlib import Path
from unittest import main
from unittest import TestCase

from . import app_factory
from . import Auth
from . import get_logfile
from basic.db import get_db
from basic.gallery import get_work


class TestGallery(TestCase):
    def setUp(self):
        self.app, self.db_fake, self.db_path = app_factory()
        self.client = self.app.test_client()
        self.auth = Auth(self.client)

    def tearDown(self):
        os.close(self.db_fake)
        os.unlink(self.db_path)

    def test_path(self):
        self.assertIn(b'New design', self.app.test_client().get('/').data)

    def test_index_without_login(self):
        resp = self.client.get('/')
        self.assertIn(b'Log In', resp.data)
        self.assertIn(b'Register', resp.data)

    def test_index_login(self):
        self.auth.login()
        resp = self.client.get('/')
        self.assertIn(b'Log Out', resp.data)

    def test_create_login_required(self):
        self.assertEqual(self.client.get('/create').status_code, 403)

    def test_create_login_required_like_admin(self):
        self.auth.login('admin', 'admin')
        resp = self.client.get('/create')
        self.assertIn(b'Add work', resp.data)

    def test_create(self):
        self.auth.login('admin', 'admin')
        self.client.post(
            '/create',
            data={
                'title': 'test_image',
                'description': 'test_desc',
                'image': (io.BytesIO(b'randomstr'), 'test.jpg')
            },
            content_type='multipart/form-data'
        )
        os.remove(Path(self.app.config['UPLOAD_FOLDER']) / 'test.jpg')

    def test_index_log(self):
        self.assertIn('Works are rendered', get_logfile())

    def test_get_work(self):
        with self.app.app_context():
            self.assertEqual(get_work(1)['title'], 'Test title')

    def test__update(self):
        self.auth.login('admin', 'admin')
        self.assertEqual(self.client.get('/1/update').status_code, 200)

        self.client.post(
            '/1/update',
            data={
                'title': 'Updated',
                'description': 'updated',
                'image': (io.BytesIO(b'randomstr'), 'updated.jpg')
            },
            content_type='multipart/form-data'
        )

        with self.app.app_context():
            work = get_db().execute('SELECT * FROM work WHERE id = 1').fetchone()
            self.assertEqual(work['title'], 'Updated')

        os.remove(Path(self.app.config['UPLOAD_FOLDER']) / 'updated.jpg')

    def test_delete(self):
        self.auth.login('admin', 'admin')
        resp = self.client.post('/1/delete')
        self.assertEqual(resp.headers.get('Location'), '/')

        with self.app.app_context():
            work = get_db().execute('SELECT * FROM work WHERE id = 1').fetchone()
            self.assertIsNone(work)

        self.assertIn('Work Test title was deleted', get_logfile())

    def test_detail(self):
        resp = self.client.get('/1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Test title', resp.data)

    def test_remove_photo(self):
        self.auth.login('admin', 'admin')
        path = Path(self.app.config['UPLOAD_FOLDER']) / 'someimage.jpg'

        if not os.path.exists(path):
            os.mknod(path)

        resp = self.client.post('/1/remove_photo')
        self.assertEqual(resp.headers.get('Location'), '/')

        with self.app.app_context():
            image = get_db().execute('SELECT image FROM work WHERE id = 1').fetchone()
            self.assertIsNone(image['image'])


if __name__ == '__main__':
    main()
