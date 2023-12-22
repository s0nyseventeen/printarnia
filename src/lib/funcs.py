from pathlib import Path

from flask import current_app


def get_upload_path() -> Path:
    return Path(current_app.config['UPLOAD_FOLDER'])
