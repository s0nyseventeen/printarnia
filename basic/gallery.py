import datetime
from pathlib import Path

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('gallery', __name__)


@bp.route('/')
def index():
    works = get_db().execute('SELECT * FROM work ORDER BY created;').fetchall()
    current_app.logger.info('Works are rendered')
    return render_template('gallery/index.html', works=works)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def __create():
    if request.method == 'POST':
        title = request.form.get('title')
        created = datetime.datetime.now()
        description = request.form.get('description')
        image = request.files.get('image')
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
                (title, created, description, image.filename)
            )
            db.commit()
            image.save(Path(current_app.config['UPLOAD_FOLDER']) / image.filename)
            current_app.logger.info('Work %s is added' % title)
            return redirect(url_for('gallery.index'))
    return render_template('gallery/create.html')


def get_work(id: int):
    work = get_db().execute(
        'SELECT * FROM work WHERE id = ?;', (id,)
    ).fetchone()

    match work:
        case None:
            abort(404, f'Work id {id} does not exist')
    return work
