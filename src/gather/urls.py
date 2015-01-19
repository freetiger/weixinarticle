# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: heyuxing
'''

from django.conf.urls import patterns, url
from gather import views
urlpatterns = patterns('',
    url(r'^scan_article/(?P<weixin_info_id>\d+)/$', views.scan_article, name='scan_article'),
    url(r'^article_show/(?P<weixin_article_id>\d+)/$', views.article_show, name='article_show'),
    url(r'^scheduler/$', views.scheduler, name='scheduler'),
)


# from django.conf.urls import patterns, url
# from django.views.generic import DetailView, ListView
# from gather.job.models import Job,Scan,ScanResult
# 
# urlpatterns = patterns('',
#     url(r'^$',
#         ListView.as_view(
#             queryset=Job.objects.order_by('-create_date')[:5],
#             context_object_name='job_list',
#             template_name='gather/job/index.html'),
#         name='index'),
#     url(r'^(?P<pk>\d+)/$',
#         DetailView.as_view(
#             model=Job,
#             template_name='gather/job/detail.html'),
#         name='detail'),
#     url(r'^(?P<pk>\d+)/results/$',
#         DetailView.as_view(
#             model=Job,
#             template_name='gather/job/results.html'),
#         name='results'),
# #     url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'),
# )