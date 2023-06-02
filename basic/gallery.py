from flask import Blueprint, render_template
from .db import get_db

bp = Blueprint('gallery', __name__)


@bp.route('/')
def index():
    works = get_db().execute('SELECT * FROM work ORDER BY created;').fetchall()
    return render_template('gallery/index.html', works=works)
