import re
from django.test import TestCase

from . import post_message
from .models import Board, Message

CLEAN_RE = re.compile('^\n *|\n *$', flags=re.M)


def _clean(s):
    return CLEAN_RE.sub('', s).replace(' ', '')


class MsgTestCase(TestCase):
    def assertThreadString(self, any_msg, s):
        Message.objects.rebuild()  # TODO WTF
        res = []
        for msg in Message.objects.filter(tree_id=any_msg.tree_id):
            res.append('>' * max(msg.level-1, 0) + msg.text)

        self.assertEqual('\n'.join(res), _clean(s))


class MessageTest(MsgTestCase):
    def setUp(self):
        self.ib = Board.objects.create(uri='a', name='Animu')

    def test_basic(self):
        # No replies
        a = post_message(self.ib, 'a', None)

        self.assertIsNone(a.parent)
        self.assertIsNone(a.reply_to)
        self.assertThreadString(a, 'a')

    def test_linear(self):
        # Replies to OP
        a0 = post_message(self.ib, 'a0', None)
        post_message(self.ib, 'a1', a0)
        post_message(self.ib, 'a2', a0)
        post_message(self.ib, 'a3', a0)

        self.assertThreadString(a0, '''
                                a0
                                a1
                                a2
                                a3
                                ''')

    def test_linear2(self):
        # Replies to last msg
        a0 = post_message(self.ib, 'a0', None)
        a1 = post_message(self.ib, 'a1', a0)
        a2 = post_message(self.ib, 'a2', a1)
        a3 = post_message(self.ib, 'a3', a2)

        self.assertThreadString(a3, '''
                                a0
                                a1
                                a2
                                a3
                                ''')

    def test_linear3(self):
        # Replies to OP and last msg
        a0 = post_message(self.ib, 'a0', None)
        a1 = post_message(self.ib, 'a1', a0)
        post_message(self.ib, 'a2', a1)
        post_message(self.ib, 'a3', a0)

        self.assertThreadString(a1, '''
                                a0
                                a1
                                a2
                                a3
                                ''')

    def test_branching(self):
        a0 = post_message(self.ib, 'a0', None)
        a1 = post_message(self.ib, 'a1', a0)
        post_message(self.ib, 'a2', a1)
        post_message(self.ib, 'a3', a1)
        post_message(self.ib, 'a4', a1)

        self.assertThreadString(a0, '''
                                a0
                                a1
                                >a3
                                >a4
                                a2
                                ''')

    def test_branching2(self):
        a0 = post_message(self.ib, 'a0', None)
        a1 = post_message(self.ib, 'a1', a0)
        a2 = post_message(self.ib, 'a2', a0)
        a3 = post_message(self.ib, 'a3', a1)
        post_message(self.ib, 'a4', a1)
        post_message(self.ib, 'a5', a3)
        post_message(self.ib, 'a6', a3)

        self.assertThreadString(a2, '''
                                a0
                                a1
                                >a3
                                >>a5
                                >>a6
                                >a4
                                a2
                                ''')

    def test_branching3(self):
        ib = self.ib
        a = [post_message(ib, '@0', None)]
        a.append(post_message(ib, '@1', a[0]))
        a.append(post_message(ib, '@2', a[1]))
        a.append(post_message(ib, '@3', a[1]))
        a.append(post_message(ib, '@4', a[3]))
        a.append(post_message(ib, '@5', a[1]))
        a.append(post_message(ib, '@6', a[3]))
        a.append(post_message(ib, '@7', a[3]))
        a.append(post_message(ib, '@8', a[7]))
        a.append(post_message(ib, '@9', a[4]))

        self.assertThreadString(a[0], '''
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
