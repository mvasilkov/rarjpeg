from django.test import TestCase
from .models import Board

class ModelTest(TestCase):
    def test_board(self):
        b = Board.objects.create(uri='a', name='Animu')
        self.assertEqual(format(b), '/a/ Animu')
        self.assertEqual(b.get_absolute_url(), '/a/')
