from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from .db import get_db
from .auth import login_required
import datetime

bp = Blueprint('gallery', __name__)


@bp.route('/')
def index():
    works = get_db().execute('SELECT * FROM work ORDER BY created;').fetchall()
    return render_template('gallery/index.html', works=works)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def __create():
    if request.method == 'POST':
        title = request.form['title']
        created = datetime.datetime.now()
        description = request.form['description']
        image = request.form['image']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO work (title, created, description, image) '
                'VALUES (?, ?, ?, ?)',
                (title, created, description, image)
            )
            db.commit()
            return redirect(url_for('gallery.index'))
    return render_template('gallery/create.html')
