from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from annoying.decorators import render_to

from .ib.views import imageboard

admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^$', render_to('index.html')(lambda req: {}), name='begin'),
    ('^admin/', include('admin_honeypot.urls')),
    (getattr(settings, 'ADMIN_REGEX', '^_admin/'), include(admin.site.urls)),
    url('^([a-z]{1,20})/$', imageboard, name='imageboard'),
)

if settings.DEBUG:
    from django.contrib.staticfiles.views import serve

    urlpatterns += patterns(
        '',
        (r'^(favicon\.ico|robots\.txt)$', serve),
    )
