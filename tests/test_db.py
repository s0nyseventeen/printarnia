import os
from sqlite3 import ProgrammingError
from unittest import main
from unittest import TestCase
from unittest.mock import patch

from . import app_factory
from basic.db import get_db


class TestDb(TestCase):
    def setUp(self):
        self.app, self.db_fake, self.db_path = app_factory()
        self.runner = self.app.test_cli_runner()

    def tearDown(self):
        os.close(self.db_fake)
        os.unlink(self.db_path)

    def test_db_same_conn(self):
        with self.app.app_context():
            db = get_db()
            self.assertEqual(db, get_db())

        with self.assertRaises(ProgrammingError) as e:
            db.execute('SELECT 1')
        self.assertIn('closed database', str(e.exception))

    @patch('basic.db.init_db')
    def test_init_db_cmd(self, mock_init_db):
        mock_init_db.return_value = lambda: None
        res = self.runner.invoke(args=['init-db'])
        self.assertIn('Initialized', res.output)


if __name__ == '__main__':
    main()
