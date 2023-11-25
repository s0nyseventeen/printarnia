from functools import wraps

from flask import g
from flask import redirect
from flask import session
from flask import url_for
from werkzeug.exceptions import abort


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
