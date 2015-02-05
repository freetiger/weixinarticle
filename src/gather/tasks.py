# -*- coding: utf-8 -*-
'''
Created on 2015年2月1日

@author: heyuxing
'''
from __future__ import absolute_import

from celery import shared_task

@shared_task
def test(x, y):
    print "taks test!!!!!"

@shared_task
def add(x, y):
    print "add helllllloooo"+str(x+y)
    return x + y

@shared_task
def scan_article(weixin_info_id=None, weixin_nos=None):
    from gather import script
    if weixin_info_id is not None:
        print "task: scan_article start. weixin_info_id="+str(weixin_info_id)
        script.scan_article(weixin_info_id=weixin_info_id)
    elif weixin_nos is not None:
        weixin_no_list = weixin_nos.split(",")
        for weixin_no in weixin_no_list:
            if weixin_no.strip()!="":
                from gather.models import WeixinInfo
                weixinInfo = WeixinInfo.objects.get(weixin_no=weixin_no.strip())
                if weixinInfo and weixinInfo.weixin_name:
                    if len(weixinInfo.openid)==0:
                        weixin_infos = script.search_weixin_info(weixinInfo.weixin_name, is_all=True)
                        for weixin_info in weixin_infos:
                            if weixin_info[1]==weixinInfo.weixin_no:
                                weixinInfo.weixin_name=weixin_info[0]
                                weixinInfo.weixin_no=weixin_info[1]
                                weixinInfo.openid=weixin_info[2]
                                weixinInfo.save()
                                break
                    script.scan_article(weixin_info_id=weixinInfo.id)
                else:
                    print "scan_article: can not find weixin_no="+weixin_no
    else:
        print "scan_article: need params(weixin_info_id or weixin_nos)"
 
@shared_task   
def scan_all_article():
    from gather.models import WeixinInfo
    weixinInfoList = WeixinInfo.objects.all()
    for weixinInfo in weixinInfoList:
        scan_article(weixin_info_id=weixinInfo.id)

