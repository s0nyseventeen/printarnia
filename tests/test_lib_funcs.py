from pathlib import Path
from src.lib.funcs import get_upload_path


def test_get_upload_path(app):
    with app.app_context():
        assert str(get_upload_path()) == str(Path('src/static/images'))
