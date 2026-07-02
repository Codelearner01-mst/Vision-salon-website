import unittest
from app import create_app, db
from flask import current_app

class TestAppInitialise(unittest.TestCase):
    def setUp(self):
        # Code to set up test environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        # Code to clean up after tests
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        # Test to check if the app exists
        self.assertTrue(current_app is not None)

    def test_app_is_testing(self):
        # Test to check if the app is in testing mode
        self.assertEqual(current_app.config['TESTING'], True)