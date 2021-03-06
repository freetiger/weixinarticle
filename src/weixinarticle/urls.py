from django.conf.urls import patterns, include, url

import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings
urlpatterns = patterns('',
    url(r'^', include(xadmin.site.urls)),
    url(r'^gather/', include('gather.urls', namespace="gather")),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^admin/', include(admin.site.urls)),
)
