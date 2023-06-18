from functools import wraps

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template
from flask import session
from flask import g
from flask import abort
from flask import current_app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif not email:
            error = 'Email is required'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), email)
                )
                db.commit()
                current_app.logger.info('User %s is registered' % username)
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                error = f'User {username} is already registered'
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            current_app.logger.info('User %s is logged in' % username)
            return redirect(url_for('gallery.index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):

    @wraps(view)
    def wrapper(**kwargs):
        if g.user is None or g.user['username'] != 'admin':
            return abort(403)
        return view(**kwargs)
    return wrapper


@bp.route('/logout')
def logout():
    session.clear()
    current_app.logger.info('User is logged out')
    return redirect(url_for('gallery.index'))
