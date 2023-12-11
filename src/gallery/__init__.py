from flask import Blueprint

bp = Blueprint('gallery', __name__, template_folder='templates')

from src.gallery import create
from src.gallery import views
