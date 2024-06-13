import unittest

from costcalc import create_app
from costcalc.extensions import db


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
