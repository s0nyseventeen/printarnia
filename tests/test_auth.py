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
        self.client = self.app.test_client()
        self.auth = Auth(self.client)

    def tearDown(self):
        os.close(self.db_fake)
        os.unlink(self.db_path)

    def test_register_status_code(self):
        self.assertEqual(
            self.client.get('/auth/register').status_code,
            200
        )

    def test_register_user(self):
        resp = self.client.post(
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
        self.assertIn('User a is registered', get_logfile())

    def test_register_validate_input_missed(self):
        resp = self.client.post(
            'auth/register',
            data={'username': '', 'password': 'a', 'email': 'a@mail.ua'}
        )
        self.assertIn(b'Username is required', resp.data)

        resp = self.client.post(
            'auth/register',
            data={'username': 'a', 'password': '', 'email': 'a@mail.ua'}
        )
        self.assertIn(b'Password is required', resp.data)

        resp = self.client.post(
            'auth/register',
            data={'username': 'a', 'password': 'a', 'email': ''}
        )
        self.assertIn(b'Email is required', resp.data)

    def test_login(self):
        self.assertEqual(self.client.get('/auth/login').status_code, 200)
        resp = self.auth.login()
        self.assertEqual(resp.headers['Location'], '/')

        with self.client:
            self.client.get('/')
            self.assertEqual(session['user_id'], 1)
            self.assertEqual(g.user['username'], 'test')

        self.assertIn('User test is logged in', get_logfile())

    def test_login_input(self):
        resp = self.auth.login('a', 'testiti')
        self.assertIn(b'Incorrect username', resp.data)

    def test_logout(self):
        self.auth.login()

        with self.client:
            self.auth.logout()
            self.assertNotIn('user_id', session)


if __name__ == '__main__':
    main()
