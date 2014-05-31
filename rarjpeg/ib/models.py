from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel

THREAD_PUBDATE_SQL = '''
SELECT MAX(pubdate) FROM ib_message t WHERE t.tree_id = ib_message.tree_id
'''


class Board(models.Model):
    uri = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=40)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join((self.get_absolute_url(), self.name))

    def get_absolute_url(self):
        return self.uri.join('//')

    def get_index(self):
        ms = Message.threads.filter(lft=1).order_by('-thread_pubdate')
        return tuple(ms.values_list('tree_id', flat=True))

    class Meta:
        ordering = ('uri',)


class MsgManager(TreeManager):
    def get_queryset(self):
        return super().get_queryset().extra(select={
            'thread_pubdate': THREAD_PUBDATE_SQL
        })


class Message(MPTTModel):
    board = models.ForeignKey(Board, related_name='messages')
    text = models.TextField(blank=True)
    pubdate = models.DateTimeField(auto_now_add=True, db_index=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='@')
    reply_to = models.ForeignKey('self', null=True, blank=True)

    objects = TreeManager()
    threads = MsgManager()

    def __str__(self):
        return '>>%d' % self.pk
