from src.lib.funcs import get_upload_path


def test_get_upload_path(app):
    with app.app_context():
        assert str(get_upload_path()) == 'src/static/images'
