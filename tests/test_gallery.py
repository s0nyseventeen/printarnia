from unittest import TestCase, main
from . import app_factory, Auth
import os


class TestGallery(TestCase):
    def setUp(self):
        self.app, self.db_fake, self.db_path = app_factory()
        self.test_client = self.app.test_client()
        self.auth = Auth(self.test_client)

    def tearDown(self):
        os.close(self.db_fake)
        os.unlink(self.db_path)

    def test_path(self):
        self.assertIn(b'New design', self.app.test_client().get('/').data)

    def test_index_without_login(self):
        resp = self.test_client.get('/')
        self.assertIn(b'Log In', resp.data)
        self.assertIn(b'Register', resp.data)

    def test_index_login(self):
        self.auth.login()
        resp = self.test_client.get('/')
        self.assertIn(b'Log Out', resp.data)

    def test_create_login_required(self):
        self.assertEqual(self.test_client.get('/create').status_code, 403)

    def test_create_login_required_like_admin(self):
        self.auth.login('admin', 'admin')
        resp = self.test_client.get('/create')
        self.assertIn(b'Add work', resp.data)


if __name__ == '__main__':
    main()
