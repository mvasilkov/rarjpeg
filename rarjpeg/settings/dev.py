import dj_database_url
from .basic import *

DEBUG = TEMPLATE_DEBUG = True

DATABASES['default'] = dj_database_url.parse('postgres://rarjpeg@/rarjpeg')

SECRET_KEY = 'Not really'
