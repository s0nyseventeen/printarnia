from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from src.extensions import db
from src.gallery import bp
from src.gallery.models import Work
from src.lib.abstractview import AbstractView


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

        work.update({
            'title': request.form['title'],
            'description': request.form['description']
        })
        db.session.commit()
        return redirect(url_for('gallery.detail', id=id))


bp.add_url_rule(
    '/<int:id>/update',
    view_func=UpdateWork.as_view('UpdateWork', Work, 'update.html')
)
