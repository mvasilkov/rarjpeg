from functools import lru_cache
from .models import Board, Message


@lru_cache(1)
def get_public_boards():
    return Board.objects.filter(is_hidden=False)


def post_message(motive, **kwargs):
    if motive:
        kwargs.update(reply_to=motive, parent_id=motive.parent_id
                      if motive.parent_id and not motive.get_next_sibling()
                      else motive.pk)

    return Message.objects.create(**kwargs)
