import os

from canoe import create_app


def test_config_true():
    assert create_app({
        'TESTING': True, 'SQLALCHEMY_DATABASE_URI': os.getenv('TESTS_SHEIKHS')
    }).testing
