from flask import Blueprint

bp = Blueprint('post', __name__, template_folder='templates')

from canoe.post import views
