import os
from unittest import main
from unittest import TestCase

from flask import g
from flask import session

from . import app_factory
from . import Auth
from . import get_logfile
from basic.db import get_db


class TestAuth(TestCase):
    def setUp(self):
        self.app, self.db_fake, self.db_path = app_factory()
        self.test_client = self.app.test_client()
        self.auth = Auth(self.test_client)
        self.logfile = get_logfile()

    def tearDown(self):
        os.close(self.db_fake)
        os.unlink(self.db_path)

    def test_register_status_code(self):
        self.assertEqual(
            self.test_client.get('/auth/register').status_code,
            200
        )

    def test_register_user(self):
        resp = self.test_client.post(
            '/auth/register',
            data={'username': 'a', 'password': 'a', 'email': 'a@mail.ua'}
        )
        self.assertEqual(resp.headers['Location'], '/auth/login')

        with self.app.app_context():
            self.assertIsNotNone(
                get_db().execute(
                    "SELECT * FROM user WHERE username = 'a';"
                ).fetchone()
            )

    def test_register_validate_input_missed(self):
        resp = self.test_client.post(
            'auth/register',
            data={'username': '', 'password': 'a', 'email': 'a@mail.ua'}
        )
        self.assertIn(b'Username is required', resp.data)

        resp = self.test_client.post(
            'auth/register',
            data={'username': 'a', 'password': '', 'email': 'a@mail.ua'}
        )
        self.assertIn(b'Password is required', resp.data)

        resp = self.test_client.post(
            'auth/register',
            data={'username': 'a', 'password': 'a', 'email': ''}
        )
        self.assertIn(b'Email is required', resp.data)

    def test_login(self):
        self.assertEqual(self.test_client.get('/auth/login').status_code, 200)
        resp = self.auth.login()
        self.assertEqual(resp.headers['Location'], '/')

        with self.test_client:
            self.test_client.get('/')
            self.assertEqual(session['user_id'], 1)
            self.assertEqual(g.user['username'], 'test')

    def test_login_input(self):
        resp = self.auth.login('a', 'testiti')
        self.assertIn(b'Incorrect username', resp.data)

    def test_logout(self):
        self.auth.login()

        with self.test_client:
            self.auth.logout()
            self.assertNotIn('user_id', session)

    def test_register_log(self):
        self.assertIn('User a is registered', self.logfile)

    def test_login_log(self):
        self.assertIn('User test is logged in', self.logfile)


if __name__ == '__main__':
    main()
