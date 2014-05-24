from django.db import models
from mptt.models import MPTTModel


class Board(models.Model):
    uri = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=40)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join((self.get_absolute_url(), self.name))

    def get_absolute_url(self):
        return self.uri.join('//')

    class Meta:
        ordering = ('uri',)


class Message(MPTTModel):
    board = models.ForeignKey(Board, related_name='messages')
    text = models.TextField(blank=True)
    pubdate = models.DateTimeField(auto_now_add=True, db_index=True)
    parent = models.ForeignKey('Message', null=True, blank=True)
    reply_to = models.ForeignKey('Message', null=True, blank=True,
                                 related_name='replies')

    def __str__(self):
        return '>>%d' % self.pk
