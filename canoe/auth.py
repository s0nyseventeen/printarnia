from functools import wraps

from flask import g
from flask import redirect
from flask import session
from flask import url_for
from werkzeug.exceptions import abort

from .db import get_db


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
