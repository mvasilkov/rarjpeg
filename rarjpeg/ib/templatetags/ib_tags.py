from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import ujson

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
