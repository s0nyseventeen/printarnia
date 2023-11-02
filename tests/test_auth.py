from flask import g
from flask import session

from .conftest import DEFAULT_USER
from canoe.db import get_db


def test_register_get_request(app, client):
    assert b'Register' in client.get('/auth/register').data


def test_register_status_code(app, client):
    assert client.get('/auth/login').status_code == 200


def test_register_validate_username_missed(auth):
    resp = auth.register({'username': '', 'password': 'a', 'email': 'a@mail.ua'})
    assert b'Username is required' in resp.data


def test_register_validate_password_missed(auth):
    resp = auth.register({'username': 'a', 'password': '', 'email': 'a@mail.ua'})
    assert b'Password is required' in resp.data


def test_register_validate_email_missed(auth):
    resp = auth.register({'username': 'a', 'password': 'a', 'email': ''})
    assert b'Email is required' in resp.data


def test_register_user(auth, app):
    auth.register(DEFAULT_USER)
    with app.app_context():
        db = get_db()
        db.cur.execute(
            "SELECT * FROM users WHERE username = 'test';"
        )
        assert db.cur.fetchone() is not None


def test_register_redirect(auth):
    assert auth.register(DEFAULT_USER).headers['Location'] == '/auth/login'


def test_register_exception_uniqueness(app, auth):
    for _ in range(2):
        resp = auth.register(DEFAULT_USER)
    assert b'User test is already registered' in resp.data


def test_login_get_request(client):
    assert b'Log In' in client.get('/auth/login').data


def test_login_status_code(client):
    assert client.get('/auth/login').status_code == 200


def test_login_validate_username(auth):
    auth.register(DEFAULT_USER)
    assert b'Incorrect username' in auth.login(username='wrong_username').data


def test_login_validate_password(auth):
    auth.register(DEFAULT_USER)
    assert b'Incorrect password' in auth.login(password='wrong_password').data


def test_login_redirect(auth):
    auth.register(DEFAULT_USER)
    assert auth.login().headers['Location'] == '/'


def test_load_logged_in_user_not_loggedin(app, client):
    with app.app_context():
        client.get('/auth/login')
        assert g.user is None


def test_load_logged_in_user(auth, client):
    auth.register(DEFAULT_USER)
    auth.login()

    with client:
        client.get('/')
        assert session['user_id'] is not None


def test_login_required_not_admin(client):
    assert client.get('/create').status_code == 403


def test_login_required_admin(auth, client):
    auth.register(
        {'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ua'}
    )
    auth.login(username='admin', password='admin')
    assert client.get('/create').status_code == 200


def test_logout(auth, client):
    auth.register(DEFAULT_USER)
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
