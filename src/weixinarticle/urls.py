from django.conf.urls import patterns, include, url

import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = patterns('',
    url(r'^', include(xadmin.site.urls)),
    url(r'^gather/', include('gather.urls', namespace="gather")),
)
