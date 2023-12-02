from flask import Blueprint

bp = Blueprint('gallery', __name__, template_folder='templates')

from canoe.gallery import views
