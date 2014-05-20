from pathlib import PurePath

DATABASES = {}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_extensions',
    'admin_honeypot',
    'rarjpeg.ib',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# -- time and locale --

TIME_ZONE = 'Asia/Jerusalem'

USE_TZ = True

LANGUAGE_CODE = 'ru-RU'

USE_I18N = USE_L10N = False

# -- paths and urls --

OUR_ROOT = PurePath(__file__).parents[2]

MEDIA_ROOT = OUR_ROOT.joinpath('media').as_posix()

MEDIA_URL = '/media/'

STATIC_ROOT = OUR_ROOT.joinpath('_pub').as_posix()

STATIC_URL = '/pub/'

STATICFILES_DIRS = (OUR_ROOT.joinpath('pub').as_posix(),)

TEMPLATE_DIRS = (OUR_ROOT.joinpath('templates').as_posix(),)

ROOT_URLCONF = 'rarjpeg.urls'

# -- auth and other things --
