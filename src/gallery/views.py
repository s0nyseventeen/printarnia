import os

from flask import redirect
from flask import render_template
from flask import url_for
from werkzeug.exceptions import abort

from src.auth.views import login_required
from src.extensions import db
from src.gallery import bp
from src.gallery.models import Image
from src.gallery.models import Work
from src.lib.funcs import get_upload_path


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/<int:id>')
def detail(id):
    return render_template(
        'detail_work.html',
        work=Work.query.get_or_404(id),
        images=Image.query.filter_by(work_id=id).order_by(Image.id).all()
    )


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    work = Work.query.get(id)
    db.session.delete(work)
    db.session.commit()

    for i in work.images:
        os.remove(get_upload_path() / i.title)
    return redirect(url_for('gallery.index'))


@bp.route('/remove_photo/<int:id>', methods=('POST',))
def remove_photo(id):
    image = Image.query.get(id)
    work_id = image.work.id
    db.session.delete(image)
    db.session.commit()
    os.remove(get_upload_path() / image.title)
    return redirect(url_for('gallery.WorkImageList', id=work_id))
