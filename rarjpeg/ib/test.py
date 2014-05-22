import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings
from .models import Board, get_public_boards
from .templatetags.ib_tags import load_crc, pub, public_boards


class ModelTest(TestCase):
    def test_board(self):
        get_public_boards.cache_clear()
        b = Board.objects.create(uri='a', name='Animu')
        self.assertEqual(format(b), '/a/ Animu')
        self.assertEqual(b.get_absolute_url(), '/a/')
        self.assertCountEqual(get_public_boards(), [b])

    def test_cache(self):
        get_public_boards.cache_clear()
        self.assertNumQueries(1, lambda: len(get_public_boards()))
        self.assertNumQueries(0, lambda: len(get_public_boards()))


def _pub_re(path):
    return ('^' + re.escape(settings.STATIC_URL + path + '?crc=') +
            '[a-z0-9]{8}$')


class HelperTest(TestCase):
    def test_load_crc(self):
        with self.assertRaisesRegex(ImproperlyConfigured, 'File not found: '):
            load_crc(settings.OUR_ROOT.joinpath('WHARRGARBL'))
        with self.assertRaisesRegex(ImproperlyConfigured, 'Bad CRC file: '):
            load_crc(settings.OUR_ROOT.joinpath('requirements.txt'))
        self.assertIsInstance(load_crc(), dict)

    def test_load_crc_once(self):
        import rarjpeg.ib.templatetags.ib_tags as ib_tags
        _load_crc = ib_tags.load_crc

        def load_test(*args):
            load_test.count += 1
            return _load_crc(*args)

        ib_tags.load_crc = load_test
        load_test.count = 0

        pub('WHARRGARBL')
        self.assertEqual(load_test.count, 1)
        pub('WHARRGARBL-96')
        self.assertEqual(load_test.count, 1)

        ib_tags.load_crc = _load_crc

    def test_pub(self):
        self.assertEqual(pub('WHARRGARBL'), settings.STATIC_URL + 'WHARRGARBL')
        self.assertRegex(pub('rarjpeg.css'), _pub_re('rarjpeg.css'))

    @override_settings(DEBUG=True)
    def test_pub_debug(self):
        with self.assertRaisesRegex(ImproperlyConfigured, 'No CRC for: '):
            pub('WHARRGARBL')
        self.assertRegex(pub('rarjpeg.css'), _pub_re('rarjpeg.css'))

    def test_public_boards(self):
        get_public_boards.cache_clear()
        t, g, a = (Board.objects.create(uri=char, name=char) for char in 'tga')
        self.assertSequenceEqual(public_boards()['boards'], [a, g, t])
