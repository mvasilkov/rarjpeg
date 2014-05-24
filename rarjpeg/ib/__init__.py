from .models import Message


def post_message(board, text, rt):
    parent = (rt.parent if rt and rt.parent_id and not rt.get_next_sibling()
              else rt)
    return Message.objects.create(board=board, text=text, parent=parent,
                                  reply_to=rt)
