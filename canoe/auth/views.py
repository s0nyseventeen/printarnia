from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.views import View
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash

from canoe.auth import bp
from canoe.auth.models import Users


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if not user_id:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()


class Login(View):
    methods = ['GET', 'POST']

    def __init__(self, template: str):
        self.__template = template

    def dispatch_request(self):
        match request.method:
            case 'GET':
                return render_template(self.__template)

            case 'POST':
                username = request.form['username']
                password = request.form['password']
                error = None
                user = Users.query.filter_by(username=username).first()

                if not user:
                    error = 'Incorrect username'

                if not check_password_hash(user.password, password):
                    error = 'Incorrect password'

                if not error:
                    session.clear()
                    session['user_id'] = user.id
                    return redirect(url_for('gallery.index'))
                flash(error)


bp.add_url_rule('/auth/login', view_func=Login.as_view('auth', 'login.html'))
