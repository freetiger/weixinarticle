# -*- coding: utf-8 -*-
'''
Created on 2015年1月12日

@author: heyuxing
'''
import urllib2, cookielib, urllib
import time

class HTTPRefererProcessor(urllib2.BaseHandler):
    def __init__(self):
        self.referer = None
    
    def http_request(self, request):
        if ((self.referer is not None) and
            not request.has_header("Referer")):
            request.add_unredirected_header("Referer", self.referer)
        return request

    def http_response(self, request, response):
        self.referer = response.geturl()
        return response
        
    https_request = http_request
    https_response = http_response

    

class ErrorHandler(urllib2.HTTPDefaultErrorHandler):  
    def http_error_default(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)  
        result.status = code  
        return result
    
'''
移除html标签，特别的：br标签替换成一个空格
'''
def remove_tag(page_src,omit_tag):
    chunk_list = []
    tag_head = "<"+omit_tag
    b_pos = page_src.find(tag_head)
    e_pos = 0
    while b_pos>=0 and e_pos>=0:
        if omit_tag.startswith("br"):
            chunk_list.append(page_src[e_pos:b_pos]+" ")
        else:
            chunk_list.append(page_src[e_pos:b_pos])
        e_pos = page_src.find(">",b_pos)+1
        b_pos = page_src.find(tag_head,e_pos)
    if b_pos == -1 and e_pos >=0:
        chunk_list.append(page_src[e_pos:])
    return ''.join(chunk_list)

'''
URL特殊字符转义
'''            
def urlzhuanyi(in_url):
    in_url = in_url.replace("&amp;","&")    
    return in_url
    
'''
获得inUrl请求数据的结果htmlsrc
inUrl：请求链接
post_datas：post数据
inUrl前缀做判断：如果是文件则读取文件内容返回，如果是文本内容则直接返回该内容，如果是url则返回该url应答页面的内容。
'''
def getUrlContent(inUrl,post_datas={}, sleep_time=0):
    if sleep_time>0:
        time.sleep(sleep_time)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cj),
            HTTPRefererProcessor(),
        )
    urllib2.install_opener(opener)
        
    if len(inUrl)==0:
        #print "get blank url"
        return ""
    inUrl = urlzhuanyi(inUrl)
           
    if inUrl.startswith("file:///"):
        tmp_file = open(inUrl[8:],"r")
        filesrc = tmp_file.read()
        tmp_file.close()
        print "request: "+str(inUrl)
        return filesrc
    elif inUrl.startswith("inline:///"):
        return inUrl[10:]
       
    tpnum = 5    #url请求出错时重试多次（5次）
    headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-cn,zh;q=0.5",
            "Accept-Charset":"gb2312,utf-8;q=0.7,*;q=0.7",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Cookie":"skin=noskin; path=/; domain=.amazon.com; expires=Wed, 25-Mar-2009 08:38:55 GMT\r\nsession-id-time=1238569200l; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT\r\nsession-id=175-6181358-2561013; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT"
        }
#     if inUrl.count("weixin.sogou.com")>0:
#         headers = {
#             "Host": "weixin.sogou.com",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
#             "Accept-Encoding": "gzip, deflate",
#             "Cookie": "CXID=7B2FDDA4C4F052374394085AAD8B98A3; SUID=1EC5E7655709950A538835A0000DEB93; SUV=001B04B565E7C51E538D3B37E8AD5410; IPLOC=CN3100; ssuid=7548319840; pgv_pvi=4598510592; ABTEST=7|1421028691|v1; SNUID=CD1134B6D3D6DFB9485FEDC0D4C04012; sct=1; LSTMV=9%2C17; LCLKINT=1029035",
#             "Connection": "keep-alive",
#             }
#     elif inUrl.count("weixin.qq.com")>0:
#         headers = {
#             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#             "Accept-Encoding":"gzip,deflate,sdch",
#             "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
#             "Cache-Control":"max-age=0",
#             "Connection":"keep-alive",
#             "Cookie":"isNarrow=0; ts_refer=www.baidu.com/s; ts_uid=8624891305; RK=ENGzloj0GQ; pgv_pvi=1479056384; ptui_loginuin=378823253; sd_userid=63491421117303085; sd_cookie_crttime=1421117303085; pt2gguin=o0378823253; ptcz=fe4f9a22997c7bb50ff6c978cd1260f36f4f9af2e2f6d844c201083801254492; o_cookie=378823253; pgv_pvid=1597739945; isVideo_DC=0",
#             "Host":"mp.weixin.qq.com",
#             "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
#             "If-Modified-Since":"Wed, 14 Jan 2015 11:32:50 GMT",
#             }
#     else:
#         headers = {
#                 "Content-Type": "application/x-www-form-urlencoded",
#                 "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                 "Accept-Language":"zh-cn,zh;q=0.5",
#                 "Accept-Charset":"gb2312,utf-8;q=0.7,*;q=0.7",
#                 "Connection": "Keep-Alive",
#                 "Cache-Control": "no-cache",
#                 "Cookie":"skin=noskin; path=/; domain=.amazon.com; expires=Wed, 25-Mar-2009 08:38:55 GMT\r\nsession-id-time=1238569200l; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT\r\nsession-id=175-6181358-2561013; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT"
#             }
    req=urllib2.Request(inUrl,headers=headers) #伪造request的header头，有些网站不支持，会拒绝请求;有些网站必须伪造header头才能访问
    htmlsrc = ""
    while len(htmlsrc)==0 and tpnum>0:
        try:
            print "request: "+str(inUrl)
            import socket
            s=socket.socket()
            socket.setdefaulttimeout(25)
            s.setblocking(0)
            try:
                resp = None
                if post_datas:
                    url_data = urllib.urlencode(post_datas)
                    resp = urllib2.urlopen(req, url_data)   #inUrl
                else:
                    resp = urllib2.urlopen(req)
                code = resp.getcode()
                if code < 200 or code >= 300:
                    #你自己的HTTP错误处理
                    print "你自己的HTTP错误处理 code="+str(code)
                else:
                    print "code="+str(code)
                htmlsrc =resp.read()                
                tpnum = 0
            except Exception , e:
                print "request time out",tpnum
                import traceback
                traceback.print_exc()#将异常信息打印在解释器上
                #
                htmlsrc = ""
                tpnum = tpnum - 1
        except urllib2.URLError,err:
            print err
            return None
    return htmlsrc


if __name__ == "__main__":   
    #print getUrlContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page=1&t=1421236929826")
    print getUrlContent("http://mp.weixin.qq.com/s?__biz=MzA5NDI5ODczNA==&mid=206354655&idx=2&sn=b22f21b1d06b78955d722f53a26fbebc&3rd=MzA3MDU4NTYzMw==&scene=6#rd")
    
    
    
