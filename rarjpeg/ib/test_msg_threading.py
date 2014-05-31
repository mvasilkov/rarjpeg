from django.test import TestCase

from . import post_message
from .models import Board


class IndexTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(uri='a', name='Animu')

    def tearDown(self):
        self.board.delete()

    def msg(self, *args, **kwargs):
        return post_message(*args, board=self.board, **kwargs)

    def test_shallow(self):
        a, b, c = self.msg(False), self.msg(False), self.msg(False)

        self.assertTupleEqual(self.board.get_index(),
                              (c.tree_id, b.tree_id, a.tree_id))

    def test_bump(self):
        a, b = self.msg(False), self.msg(False)
        self.msg(a)

        self.assertTupleEqual(self.board.get_index(), (a.tree_id, b.tree_id))
