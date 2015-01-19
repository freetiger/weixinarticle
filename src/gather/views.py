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
    
def scheduler(request):
    from gather.scheduler import scheduler_scan_all_article
    scheduler_scan_all_article()#TODO
    html = "<html><body>定时任务启动. </body></html>" 
    return HttpResponse(html)



