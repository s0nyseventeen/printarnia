from functools import wraps

from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from src.auth import bp
from src.auth.models import Users
from src.extensions import db


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif not email:
            error = 'Email is required'

        if not error:
            try:
                db.session.add(Users(
                    username=username,
                    password=generate_password_hash(password),
                    email=email
                ))
                db.session.commit()
                return redirect(url_for('auth.login'))
            except IntegrityError:
                error = f'User {username} is already registered'
        flash(error)
    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = Users.query.filter_by(username=username).first()

        if not user:
            error = 'Incorrect username'

        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if not error:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('gallery.index'))
        flash(error)
    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()


def login_required(view):

    @wraps(view)
    def wrapper(**kwargs):
        if not g.get('user') or g.user.username != 'admin':
            return abort(403)
        return view(**kwargs)
    return wrapper


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gallery.index'))
