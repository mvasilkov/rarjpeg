from django.db import models
from functools import lru_cache

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

@lru_cache(1)
def get_public_boards():
    return Board.objects.filter(is_hidden=False)
