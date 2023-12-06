from flask import Blueprint

bp = Blueprint(
    'auth', __name__, url_prefix='/auth', template_folder='templates'
)

from src.auth import views
