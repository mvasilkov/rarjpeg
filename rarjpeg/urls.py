from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(favicon\.ico|robots\.txt)$', serve),
)
