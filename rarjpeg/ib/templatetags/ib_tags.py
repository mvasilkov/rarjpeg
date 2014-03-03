from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import ujson
from ..models import get_public_boards

CRC = {}

def load_crc(path=settings.OUR_ROOT.child('_pub.json')):
    try:
        with open(path, encoding='utf8') as crc_file:
            return ujson.loads(crc_file.read())
    except FileNotFoundError:
        raise ImproperlyConfigured('File not found: ' + path)
    except ValueError:
        raise ImproperlyConfigured('Bad CRC file: ' + path)

def pub(path):
    global CRC
    if not CRC:
        CRC = load_crc()
    path_gz = path + '.gz'
    if path_gz in CRC:
        path = path_gz
    try:
        crc = '?crc=' + CRC[path]
    except KeyError:
        if settings.DEBUG:
            raise ImproperlyConfigured('No CRC for: ' + path)
        else:
            crc = ''
    return ''.join((settings.STATIC_URL, path, crc))

register = template.Library()
register.simple_tag(pub)

def public_boards():
    return {'boards': get_public_boards()}

register.inclusion_tag('_public_boards.html')(public_boards)
