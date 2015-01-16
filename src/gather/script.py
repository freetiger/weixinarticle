# -*- coding: utf-8 -*-
'''
Created on 2015年1月12日

@author: heyuxing
'''
import datetime
from gather import utils, dbutils
import re


'''
http://weixin.sogou.com 搜索的结果页的页数，并不准确，需要逼近最后一页确定总页数
'''
def get_page_total(openid):
    page_total = 1
    page_current = 1
    param_retrieve_str = re.compile(r'"totalPages":(\d*),"page":(\d*)')
    while True:
        page_src = utils.getUrlContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid="+openid+"&page="+str(page_current), sleep_time=0.3)
        params = param_retrieve_str.findall(page_src)
        if len(params)==0:
            print "get_page_total error!"
            break
        page_total = int(params[0][0])
        page_current = int(params[0][1])
        if(page_current>=page_total):
            break
        else:
            page_current = page_total
    print "page_total="+str(page_total)
    return page_total     

'''
获得搜狗上微信账号openid的所有文章列表页
'''
def get_article_list_urls(openid, page_total=1):
    base_url = "http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid="+openid+"&page="
    article_list_urls = []
    for index in range(page_total):
        article_list_urls.append(base_url+str(index+1))
    return article_list_urls

'''
扫描搜狗上微信账号的文章列表页，获得文章标题title和文章链接url
'''
def scan_article_list(article_list_urls):
    article_urls = []
    for article_list_url in article_list_urls:
        page_src = utils.getUrlContent(article_list_url, sleep_time=0.3)
        regular_str = re.compile(r'<title><\!\[CDATA\[([^]]*)\]\]><[^/]*/title><url><\!\[CDATA\[([^]]*)' )
        datas = regular_str.findall(page_src)
        for data in datas:
            article_urls.append({"title":data[0], "url":data[1], } )
    return article_urls

'''
抓取微信weixin_info_id的文章内容，article_urls为文章标题title和链接url
'''
def scan_article_content(article_urls, weixin_info_id):
    count =0
    for article_url in article_urls:
        title = article_url.get("title")
        url = article_url.get("url")
        content = utils.getUrlContent(url, sleep_time=0.3)
        dbutils.saveWeixinArticle(weixin_info_id, title, url, content)
        count=count+1
    return count

'''
过滤掉已抓取过的文章链接
'''
def article_urls_filter(article_urls, weixin_info_id):
    urls = dbutils.getWeixinArticleUrls(weixin_info_id)
    temp_article_urls = []
    for article_url in article_urls:
        if article_url.get("url") not in urls:
            temp_article_urls.append(article_url)
    return temp_article_urls
    
'''
扫描指定微信公众账号的文章
weixin_info_id：微信信息表WeixinInfo的id
openid：微信公众账号的openid
is_add：是否增量扫描，默认是True
'''
def scan_article(weixin_info_id=None, openid=None, is_add=True):
    if weixin_info_id is None and openid is None:
        print "scan_article need params(weixin_info_id or openid)!"
        return
    elif weixin_info_id is not None:
        weixinInfoList = dbutils.getWeixinInfoList(id=weixin_info_id)
    else:
        weixinInfoList = dbutils.getWeixinInfoList(openid=openid)
    for weixinInfo in weixinInfoList:
        weixin_info_id = weixinInfo.id
        openid = weixinInfo.openid
        page_total = get_page_total(openid)
        article_list_urls = get_article_list_urls(openid, page_total)
        article_urls = scan_article_list(article_list_urls)
        if is_add:
            article_urls = article_urls_filter(article_urls, weixin_info_id)
        update_num = scan_article_content(article_urls, weixin_info_id)
        #抓取时间和文章数更新
        dbutils.updateWeixinInfoById(id=weixin_info_id, last_scan_date=str(datetime.datetime.now()), update_num=update_num)
    #
    return ""

'''
搜索keyword相关的微信号，weixin_name、weixin_no、openid
'''
def search_weixin_info(keyword):
    import urllib
    weixin_infos = []
    page_src = utils.getUrlContent("http://weixin.sogou.com/weixin?type=1&"+urllib.urlencode({"query":keyword}))
    page_src = utils.remove_tag(page_src, "em")
    page_src = utils.remove_tag(page_src, "/em")
    page_src = utils.remove_tag(page_src, "!--red_beg--")
    page_src = utils.remove_tag(page_src, "!--red_end--")
    regular_str = re.compile(r'<h3>([^<]*)</h3>[^<]*<h4>[^<]*<span>微信号：([^<]*)</span>')
    datas = regular_str.findall(page_src)
    #openid
    openid_regular_str = re.compile(r'gotourl\(\'/gzh\?openid=([^\']*)')
    openids = openid_regular_str.findall(page_src)
    if len(datas)==len(openids):
        for index in range(len(datas)):
            weixin_infos.append((datas[index][0], datas[index][1], openids[index]), )
    else:
        print "search_weixin_info("+keyword+") error! len(datas)="+str(len(datas))+", len(openids)="+str(len(openids))
    
    return weixin_infos

if __name__ == "__main__":   
    #scan_article(openid="oIWsFt-Atb62Noyz4nKX1nvrmFHQ")
    print search_weixin_info("罗辑思维")
        
        
    