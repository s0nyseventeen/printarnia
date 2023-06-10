from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg')

    if test_config is not None:
        app.config.from_mapping(test_config)

    from .db import init_app
    init_app(app)

    from .auth import bp
    app.register_blueprint(bp)

    from .gallery import bp
    app.register_blueprint(bp)

    return app
