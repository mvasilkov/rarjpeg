import os.path

DATABASES = {}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TIME_ZONE = 'Asia/Jerusalem'

USE_TZ = True

LANGUAGE_CODE = 'ru-RU'

USE_I18N = USE_L10N = False

OUR_ROOT = os.path.realpath(os.path.dirname(__file__) + '/../..')

path_to = lambda s: os.path.join(OUR_ROOT, s)

MEDIA_ROOT = path_to('media')
MEDIA_URL = '/media/'

STATIC_ROOT = path_to('_pub')
STATIC_URL = '/pub/'

STATICFILES_DIRS = (path_to('pub'),)

ROOT_URLCONF = 'rarjpeg.urls'
