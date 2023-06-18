from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    current_app,
    redirect,
    url_for
)
from .db import get_db
from .auth import login_required
import datetime
from pathlib import Path

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
