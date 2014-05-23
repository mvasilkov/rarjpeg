from annoying.decorators import render_to
from django.shortcuts import get_object_or_404

from .models import Board


@render_to('imageboard.html')
def imageboard(request, uri):
    ib = get_object_or_404(Board, uri=uri)
    return {'ib': ib}
