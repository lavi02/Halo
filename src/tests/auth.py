import unittest

from example.src.service.jwt import AuthManager
from datetime import timedelta

class TestAuthManager(unittest.TestCase):
    def test_verify_password(self):
        password = "my_password"
        hashed_password = AuthManager.get_password_hash(password)
        self.assertTrue(AuthManager.verify_password(password, hashed_password))
        self.assertFalse(AuthManager.verify_password("wrong_password", hashed_password))

    def test_get_password_hash(self):
        password = "my_password"
        hashed_password = AuthManager.get_password_hash(password)
        self.assertIsNotNone(hashed_password)
        self.assertNotEqual(hashed_password, password)

    def test_create_access_token(self):
        data = {"sub": "test_user"}
        token = AuthManager.create_access_token(data, timedelta(minutes=15))
        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 0)

if __name__ == '__main__':
    unittest.main()
