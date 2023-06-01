from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg')

    from .db import init_app
    init_app(app)

    from .auth import bp
    app.register_blueprint(bp)

    return app
