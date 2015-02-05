# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: heyuxing
'''
from django.http import HttpResponse

from gather import script
from gather.models import WeixinArticle

def scan_article(request, weixin_info_id):
    message = script.scan_article(weixin_info_id=weixin_info_id)
    html = "<html><body>扫描结束. %s</body></html>" % message
    return HttpResponse(html)

def article_show(request, weixin_article_id):
    weixinArticle = WeixinArticle.objects.get(pk=weixin_article_id)
    if weixinArticle is None:
        return "未找到文章"
    else:
        return HttpResponse(weixinArticle.content)
   
def remote_scan_article(request, weixin_nos):
    print "remote_scan_article: weixin_nos="+str(weixin_nos)
    from tasks import scan_article
    scan_article.delay(weixin_nos=weixin_nos)
    html = "success" 
    return HttpResponse(html)
 
def remote_add_weixin_info(request, weixin_nos):
    print "remote_add_weixin_info: weixin_nos="+str(weixin_nos)
    weixin_no_list = weixin_nos.split("|")
    for weixin_no in weixin_no_list:
        if weixin_no.strip()!="":
            print "weixin_no="+str(weixin_no)
    html = "success"
    return HttpResponse(html)



