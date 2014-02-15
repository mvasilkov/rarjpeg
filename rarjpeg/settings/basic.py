from unipath import Path
from .util import username

DATABASES = {}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_browserid',
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
    'django_browserid.auth.BrowserIDBackend',
)

# -- time and locale --

TIME_ZONE = 'Asia/Jerusalem'

USE_TZ = True

LANGUAGE_CODE = 'ru-RU'

USE_I18N = USE_L10N = False

# -- paths and urls --

OUR_ROOT = Path(__file__).ancestor(3)

MEDIA_ROOT = OUR_ROOT.child('media')

MEDIA_URL = '/media/'

STATIC_ROOT = OUR_ROOT.child('_pub')

STATIC_URL = '/pub/'

STATICFILES_DIRS = (OUR_ROOT.child('pub'),)

TEMPLATE_DIRS = (OUR_ROOT.child('templates'),)

ROOT_URLCONF = 'rarjpeg.urls'

LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL_FAILURE = LOGOUT_REDIRECT_URL = '/'

# -- auth and other things --

BROWSERID_USERNAME_ALGO = username
