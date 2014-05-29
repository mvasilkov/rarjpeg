from unittest import TestCase
from django.core.exceptions import ImproperlyConfigured
from .util import username, env


class UtilTest(TestCase):
    def test_username(self):
        self.assertEqual(username('rememberingsteve@apple.com'),
                         'rememberingsteve+1eabe9c2')
        self.assertEqual(username('benedictxvi@vatican.va'),
                         'benedictxvi+1e33c678')
        self.assertEqual(username('"burn@the"@heretic'),
                         '"burn@the"+8f5d023b')

    def test_env(self):
        self.assertEqual(env.DJANGO_SETTINGS_MODULE, 'rarjpeg.settings')

        self.assertIsInstance(env.HOME, str)

        with self.assertRaises(ImproperlyConfigured):
            res = env.WHARRGARBL
            print(res)
