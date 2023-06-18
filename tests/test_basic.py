import os
from unittest import main
from unittest import TestCase

from basic import create_app
from . import app_factory


class BasicTest(TestCase):
    def setUp(self):
        self.app, self.db_fake, self.db_path = app_factory()
        self.runner = self.app.test_cli_runner()

    def tearDown(self):
        os.close(self.db_fake)
        os.unlink(self.db_path)

    def test_config(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)


if __name__ == '__main__':
    main()
