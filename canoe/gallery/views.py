import datetime
import os
from pathlib import Path

from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from canoe.auth.views import login_required
from canoe.extensions import db
from canoe.gallery import bp
from canoe.gallery.models import Work


@bp.route('/')
def index():
    return render_template('index.html', works=Work.query.all())


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        created = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        description = request.form.get('description')
        image = request.files.get('image')

        if not title:
            flash('Title is required')
            return render_template('create.html')

        if not check_image_exists(image):
            db.session.add(Work(
                title=title, created=created, description=description
            ))
            db.session.commit()
            return redirect(url_for('gallery.index'))

        db.session.add(Work(
            title=title,
            created=created,
            description=description,
            image=image.filename
        ))
        db.session.commit()
        image.save(Path(current_app.config['UPLOAD_FOLDER']) / image.filename)
        return redirect(url_for('gallery.index'))
    return render_template('create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files.get('image')

        if not check_image_exists(image):
            Work.query.filter_by(id=id).update(
                dict(title=title, description=description)
            )
            db.session.commit()
            return redirect(url_for('gallery.detail', id=id))

        Work.query.filter_by(id=id).update(
            dict(title=title, description=description, image=image.filename)
        )
        db.session.commit()
        image.save(Path(current_app.config['UPLOAD_FOLDER']) / image.filename)
        return redirect(url_for('gallery.detail', id=id))

    return render_template('update.html', work=get_work(id))


@bp.route('/<int:id>')
def detail(id):
    return render_template('detail.html', work=get_work(id))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    Work.query.filter_by(id=id).delete()
    return redirect(url_for('gallery.index'))


@bp.route('/<int:id>/remove_photo', methods=('POST',))
def remove_photo(id):
    work_image = get_work(id).image
    Work.query.filter_by(id=id).update(dict(image=None))
    db.session.commit()
    os.remove(Path(current_app.config['UPLOAD_FOLDER']) / work_image)
    return redirect(url_for('gallery.index'))


def get_work(id):
    work = Work.query.filter_by(id=id).first()

    if not work:
        abort(404, f'Work id {id} does not exist')
    return work


def check_image_exists(image) -> bool:
    return image.filename != ''
