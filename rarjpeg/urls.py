from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from annoying.decorators import render_to

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', render_to('index.html')(lambda req: {})),
    url(r'', include('django_browserid.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(favicon\.ico|robots\.txt)$', serve),
)
