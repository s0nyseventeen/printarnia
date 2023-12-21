from abc import ABC

from flask.views import View

from src.auth.views import login_required


class AbstractView(ABC, View):
    init_every_request = False
    decorators = [login_required]
