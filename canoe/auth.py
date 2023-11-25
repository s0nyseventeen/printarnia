from flask import redirect
from flask import session
from flask import url_for


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gallery.index'))
