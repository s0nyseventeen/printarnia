import datetime
from pathlib import Path

from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from src.extensions import db
from src.gallery import bp
from src.gallery.models import Image
from src.gallery.models import Work
from src.lib.abstractview import AbstractView
from src.lib.request_helpers import get_img_info


class Create(AbstractView):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'GET':
            return render_template('create.html')

        title = request.form.get('title')
        if not title:
            flash('Title is required')
            return render_template('create.html')

        new_work = Work(
            title=title,
            created=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            description=request.form.get('description')
        )
        img, description = get_img_info(request)
        if not img:
            db.session.add(new_work)
            db.session.commit()
            return redirect(url_for('gallery.index'))

        new_image = Image(
            title=img.filename, description=description, work=new_work
        )
        db.session.add(new_image)
        db.session.commit()
        img.save(Path(current_app.config['UPLOAD_FOLDER']) / img.filename)
        return redirect(url_for('gallery.index'))


bp.add_url_rule('/create', view_func=Create.as_view('create'))
