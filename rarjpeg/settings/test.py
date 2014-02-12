from unittest import TestCase
from .util import username

class UsernameTest(TestCase):
    def test_username(self):
        self.assertEqual(username('rememberingsteve@apple.com'),
                         'rememberingsteve+1eabe9c2')
        self.assertEqual(username('benedictxvi@vatican.va'),
                         'benedictxvi+1e33c678')
        self.assertEqual(username('"burn@the"@heretic'),
                         '"burn@the"+8f5d023b')
