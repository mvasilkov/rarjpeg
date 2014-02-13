from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from annoying.decorators import render_to

admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^$', render_to('index.html')(lambda req: {})),
    ('', include('django_browserid.urls')),
    ('^admin/', include('admin_honeypot.urls')),
    (getattr(settings, 'ADMIN_REGEX', '^_admin/'), include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.views import serve

    urlpatterns += patterns(
        '',
        (r'^(favicon\.ico|robots\.txt)$', serve),
    )
