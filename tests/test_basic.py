from canoe import create_app


def test_config_false():
    assert create_app().testing is False


def test_config_true():
    assert create_app({'TESTING': True}).testing is True
