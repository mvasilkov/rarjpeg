from django.test import TestCase
from .models import Board, get_public_boards

class ModelTest(TestCase):
    def test_board(self):
        b = Board.objects.create(uri='a', name='Animu')
        self.assertEqual(format(b), '/a/ Animu')
        self.assertEqual(b.get_absolute_url(), '/a/')
        self.assertCountEqual(get_public_boards(), [b])

    def test_cache(self):
        get_public_boards.cache_clear()
        self.assertNumQueries(1, lambda: len(get_public_boards()))
        self.assertNumQueries(0, lambda: len(get_public_boards()))
