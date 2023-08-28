import datetime
import os
from pathlib import Path
from typing import Any

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg2.sql import Identifier
from psycopg2.sql import Literal
from psycopg2.sql import SQL
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('gallery', __name__)


@bp.route('/')
def index():
    works = get_db().execute('SELECT * FROM work ORDER BY created DESC;').fetchall()
    current_app.logger.info('Works are rendered')
    return render_template('gallery/index.html', works=works)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        db = get_db()
        title = request.form.get('title')
        created = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        description = request.form.get('description')
        image = request.files.get('image')

        if not title:
            flash('Title is required')

        if __check_image(image):
            db.run_query(
                SQL('''
                    INSERT INTO {table} (title, created, description)
                    VALUES ({title}, {created}, {description});'''
                ).format(
                    table=Identifier('work'),
                    title=Literal(title),
                    created=Literal(created),
                    description=Literal(description)
                )
            )
            current_app.logger.info('Work %s is added' % title)
            return redirect(url_for('gallery.index'))

        db.run_query(
            SQL('''
                INSERT INTO {table} (title, created, description, image)
                VALUES ({title}, {created}, {description}, {image});'''
            ).format(
                table=Identifier('work'),
                title=Literal(title),
                created=Literal(created),
                description=Literal(description),
                image=Literal(image.filename)
            )
        )
        image.save(Path(current_app.config['UPLOAD_FOLDER']) / image.filename)
        return redirect(url_for('gallery.index'))
    return render_template('gallery/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    work = get_work(id)
    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files.get('image')

        if __check_image(image):
            db.run_query(
                SQL('''
                    UPDATE {table} SET title = {title}, description = {description}
                    WHERE id = {id};'''
                ).format(
                    table=Identifier('work'),
                    title=Literal(title),
                    description=Literal(description),
                    id=Literal(id)
                )
            )
            current_app.logger.info('Work %s was updated' % title)
            return redirect(url_for('gallery.index'))

        db.run_query(
            SQL('''
                UPDATE {table} SET title = {title},
                    description = {description},
                    image = {image}
                WHERE id = {id};'''
            ).format(
                table=Identifier('work'),
                title=Literal(title),
                description=Literal(description),
                image=Literal(image.filename),
                id=Literal(id)
            )
        )
        image.save(Path(current_app.config['UPLOAD_FOLDER']) / image.filename)
        return redirect(url_for('gallery.index'))
    return render_template('gallery/update.html', work=work)


@bp.route('/<int:id>')
def detail(id):
    return render_template('gallery/work.html', work=get_work(id))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    work = get_work(id)
    db = get_db()
    db.run_query(
        SQL('DELETE FROM {table} WHERE id = {id};').format(
            table=Identifier('work'), id=Literal(id)
        )
    )
    current_app.logger.info('Work %s was deleted', work[1])
    return redirect(url_for('gallery.index'))


@bp.route('/<int:id>/remove_photo', methods=('POST',))
def remove_photo(id):
    work = get_work(id)
    db = get_db()
    db.run_query(
        SQL('UPDATE {table} SET image = NULL WHERE id = {id};').format(
            table=Identifier('work'), id=Literal(id)
        )
    )
    os.remove(Path(current_app.config['UPLOAD_FOLDER']) / work[4])
    return redirect(url_for('gallery.index'))


def get_work(id):
    work = get_db().execute(
        'SELECT * FROM work WHERE id = ?;', (id,)
    ).fetchone()

    if work is None:
        abort(404, f'Work id {id} does not exist')
    return work


def __check_image(image) -> bool:
    return image.filename == ''
