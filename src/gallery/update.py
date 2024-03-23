import os

from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from src import db
from src.gallery import bp
from src.gallery.models import Image
from src.gallery.models import Work
from src.lib.abstractview import AbstractView
from src.lib.funcs import get_upload_path
from src.lib.request_helpers import get_img_info


class AbstractUpdate(AbstractView):
    def __init__(self, model, template):
        self.model = model
        self.template = template


class UpdateWork(AbstractUpdate):
    methods = ['GET', 'POST']

    def dispatch_request(self, id):
        work = self.model.query
        if request.method == 'GET':
            return render_template(self.template, work=work.get_or_404(id))

        work = work.get(id)
        work.title = request.form['title'],
        work.description = request.form['description']
        db.session.commit()
        return redirect(url_for('gallery.detail', id=id))


class WorkImageList(AbstractUpdate):
    def __init__(self, model, image, template):
        super().__init__(model, template)
        self.__image = image

    def dispatch_request(self, id):
        return render_template(
            self.template,
            work=self.model.query.get_or_404(id),
            images=self.__image.query.filter_by(work_id=id).order_by(Image.id).all()
        )


class AddWorkImage(AbstractUpdate):
    methods = ['GET', 'POST']

    def __init__(self, model, image, template):
        super().__init__(model, template)
        self.image = image

    def dispatch_request(self, id):
        work = self.model.query.get_or_404(id)
        if request.method == 'GET':
            return render_template(self.template, work=work)

        image = request.files.get('image')
        if image:
            description = request.form.get('image_description')
            new_image = self.image(
                title=image.filename,
                description=description,
                work=self.model.query.get_or_404(id)
            )
            db.session.add(new_image)
            db.session.commit()
            image.save(get_upload_path() / image.filename)
            return redirect(url_for('gallery.WorkImageList', id=id))

        flash('Please add a file')
        return render_template(self.template, work=work)


class DetailImage(AbstractUpdate):
    methods = ['GET', 'POST']

    def dispatch_request(self, work_id, image_id):
        image = self.model.query.get_or_404(image_id)
        if request.method == 'GET':
            return render_template(self.template, image=image)

        img, description = get_img_info(request)
        if img:
            old_filename = image.title
            new_filename = img.filename
            image.title = new_filename
            path = get_upload_path()
            img.save(path / new_filename)
            os.remove(path / old_filename)

        old_description = image.description
        if description != old_description:
            image.description = description

        db.session.commit()
        return redirect(url_for('gallery.WorkImageList', id=work_id))


bp.add_url_rule(
    '/<int:id>/update',
    view_func=UpdateWork.as_view('UpdateWork', Work, 'update.html')
)
bp.add_url_rule(
    '/<int:id>/update/images',
    view_func=WorkImageList.as_view('WorkImageList', Work, Image, 'images_list.html')
)
bp.add_url_rule(
    '/<int:id>/update/images/add_image',
    view_func=AddWorkImage.as_view('AddWorkImage', Work, Image, 'add_image.html')
)
bp.add_url_rule(
    '/<int:work_id>/update/images/detail/<int:image_id>',
    view_func=DetailImage.as_view('DetailImage', Image, 'detail_image.html')
)
