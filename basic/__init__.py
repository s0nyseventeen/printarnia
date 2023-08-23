from logging.config import dictConfig

from flask import Flask

dictConfig({
    'version': 1,
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    'loggers': {
        'basic': {
            'handlers': ['basic_handler'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'basic_handler': {
            'class': 'logging.FileHandler',
            'filename': 'basic.log',
            'level': 'INFO',
            'formatter': 'default'
        }
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(module)s - %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        }
    },
})


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg')

    if test_config:
        app.config.from_mapping(test_config)

    from .auth import bp
    app.register_blueprint(bp)

    from .gallery import bp
    app.register_blueprint(bp)

    return app
