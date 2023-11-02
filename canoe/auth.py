from functools import wraps

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from psycopg2.errors import UniqueViolation
from psycopg2.sql import Identifier
from psycopg2.sql import Literal
from psycopg2.sql import SQL
from werkzeug.exceptions import abort
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

        if not error:
            try:
                db.run_query(
                    SQL("""
                        INSERT INTO {table} (username, password, email)
                        VALUES ({username}, {password}, {email});"""
                    ).format(
                        table=Identifier('users'),
                        username=Literal(username),
                        password=Literal(generate_password_hash(password)),
                        email=Literal(email)
                    )
                )
                return redirect(url_for('auth.login'))
            except UniqueViolation:
                error = f'User {username} is already registered'
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        db = get_db()
        db.cur.execute(
            SQL("SELECT * FROM {table} WHERE username = {username};").format(
                table=Identifier('users'), username=Literal(username)
            )
        )
        user = db.cur.fetchone()

        if not user:
            error = 'Incorrect username'

        elif not check_password_hash(user[3], password):
            error = 'Incorrect password'

        if not error:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('gallery.index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db = get_db()

    if not user_id:
        g.user = None
    else:
        db.cur.execute(
            SQL('SELECT * FROM {table} WHERE id = {user_id};').format(
                table=Identifier('users'), user_id=Literal(user_id)
            )
        )
        g.user = db.cur.fetchone()


def login_required(view):

    @wraps(view)
    def wrapper(**kwargs):
        if not g.get('user') or g.user[1] != 'admin':
            return abort(403)
        return view(**kwargs)
    return wrapper


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gallery.index'))
