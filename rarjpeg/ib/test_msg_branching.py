import re
from django.test import TestCase

from . import post_message
from .models import Board, Message

CLEAN_RE = re.compile('^\n *|\n *$', flags=re.M)


class MessageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = Board.objects.create(uri='a', name='Animu')

    @classmethod
    def tearDownClass(cls):
        cls.board.delete()

    @classmethod
    def _msg(cls, *args, **kwargs):
        return post_message(*args, board=cls.board, **kwargs)

    def setUp(self):
        self.a = [self.__class__._msg(False, text='@0')]

    def msg(self, *args):
        for n in args:
            self.a.append(self._msg(self.a[n], text='@%d' % len(self.a)))

    def assertLooksLikeASCII(self, s):
        res = []
        for msg in Message.objects.filter(tree_id=self.a[0].tree_id):
            res.append('>' * max(msg.level - 1, 0) + msg.text)

        self.assertListEqual(res, CLEAN_RE.sub('', s).split())

    # No replies
    def test_basic(self):
        self.assertLooksLikeASCII('@0')

    # Replies to OP
    def test_linear(self):
        self.msg(0)
        self.msg(0)
        self.msg(0)

        self.assertLooksLikeASCII('''
                                  @0
                                  @1
                                  @2
                                  @3
                                  ''')

    # Replies to last msg
    def test_linear2(self):
        self.msg(0)
        self.msg(1)
        self.msg(2)

        self.assertLooksLikeASCII('''
                                  @0
                                  @1
                                  @2
                                  @3
                                  ''')

    # Replies to OP and last msg
    def test_linear3(self):
        self.msg(0)
        self.msg(1)
        self.msg(0)

        self.assertLooksLikeASCII('''
                                  @0
                                  @1
                                  @2
                                  @3
                                  ''')

    def test_branching(self):
        self.msg(0)
        self.msg(1)
        self.msg(1)
        self.msg(1)

        self.assertLooksLikeASCII('''
                                  @0
                                  @1
                                  >@3
                                  >@4
                                  @2
                                  ''')

    def test_branching2(self):
        self.msg(0)
        self.msg(0)
        self.msg(1)
        self.msg(1)
        self.msg(3)
        self.msg(3)

        self.assertLooksLikeASCII('''
                                  @0
                                  @1
                                  >@3
                                  >>@5
                                  >>@6
                                  >@4
                                  @2
                                  ''')

    def test_branching3(self):
        self.msg(0)
        self.msg(1)
        self.msg(1)
        self.msg(3)
        self.msg(1)
        self.msg(3)
        self.msg(3)
        self.msg(7)
        self.msg(4)

        self.assertLooksLikeASCII('''
                                  @0
                                  @1
                                  >@3
                                  >>@6
                                  >>@7
                                  >>@8
                                  >@4
                                  >>@9
                                  >@5
                                  @2
                                  ''')
