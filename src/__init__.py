import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping({
            'UPLOAD_FOLDER': 'src/static/images',
            'SECRET_KEY': os.getenv('SECRET_KEY'),
            'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI')
        })

    from .extensions import db
    db.init_app(app)

    from .auth import bp
    app.register_blueprint(bp)

    from .gallery import bp
    app.register_blueprint(bp)

    return app
