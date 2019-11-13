import os
from flask import current_app
from groundstation.tests.base import BaseTestCase

# TODO: Need to test different configurations, which means creating new apps with different configs, for now this is fine

class TestTestingConfig(BaseTestCase):

    def test_app_is_testing(self):
        self.assertEqual(current_app.config['BCRYPT_LOG_ROUNDS'], 4)
        self.assertEqual(current_app.config['SECRET_KEY'], os.getenv('SECRET_KEY'))
        self.assertEqual(current_app.config['TOKEN_EXPIRATION_DAYS'], 0)
        self.assertEqual(current_app.config['TOKEN_EXPIRATION_SECONDS'], 3)
