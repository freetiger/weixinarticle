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
    
proxies=[
"163.177.79.4:80",
"223.68.6.10:8000",
"183.221.187.231:8123",
"58.253.238.243:80",
"106.37.177.251:3128",
"101.4.60.43:80",
"58.214.5.229:80",
"60.12.235.47:3128",
"183.221.190.247:8123",
"183.221.220.246:8123",
"183.224.1.30:80",
"58.253.238.242:80",
"183.207.232.194:8080",
"61.156.35.2:3128",
"218.203.13.172:80",
"183.221.174.129:8123",
"111.13.12.216:80",
"61.232.6.164:8081",
"221.12.173.130:3128",
"125.88.255.144:80",
"220.231.32.195:3128",
"36.250.69.4:80",
"60.13.74.196:80",
"218.65.132.38:80",
"183.207.232.193:8080",
"115.238.250.23:2222",
"222.88.236.236:82",
"58.240.65.57:3128",
"117.79.64.84:80",
"61.54.221.200:3128",
"121.10.252.139:3128",
"122.225.106.40:80",
"111.161.126.99:80",
"120.202.249.230:80",
"220.181.32.106:80",
"123.7.78.176:9999",
"210.82.92.77:3128",
"202.108.23.247:80",
"111.206.81.248:80",
"183.207.228.9:89",
"121.12.167.197:3128",
"58.214.19.126:9999",
"218.207.172.236:80",
"117.21.192.7:80",
"219.223.190.90:3128",
"183.129.194.87:3128",
"124.95.163.102:80",
"115.239.210.199:80",
"117.21.192.9:80",
"111.161.126.101:80",
"183.221.217.50:8123",
"140.249.10.167:8585",
"117.21.192.10:80",
"202.101.96.154:8888",
"211.144.81.69:18000",
"115.231.96.120:80",
"218.59.144.95:80",
"114.215.237.93:3128",
"120.83.5.164:18000",
"122.200.90.172:3128",
"111.13.12.202:80",
"218.207.102.107:80",
"122.136.46.151:80",
"112.65.44.71:3128",
"122.225.106.36:80",
"183.221.164.235:8123",
"123.138.76.77:18186",
"183.221.191.27:8123",
"113.106.93.42:3128",
"218.4.236.117:80",
"218.203.13.176:80",
"218.203.13.169:8090",
"183.221.220.78:8123",
"211.144.81.68:18000",
"117.135.244.41:80",
"183.221.160.238:8123",
"14.18.16.67:80",
"183.221.186.215:8123",
"125.39.66.69:80",
"183.221.175.102:8123",
"60.194.14.144:82",
"218.90.174.167:3128",
"111.161.126.98:80",
"183.221.185.227:8123",
"222.85.1.123:8118",
"113.105.224.86:80",
"163.23.70.129:3128",
"183.221.164.151:8123",
"125.39.66.68:80",
"120.199.249.241:8123",
"221.182.62.115:9999",
"183.207.228.8:80",
"218.203.13.190:80",
"117.21.192.8:80",
"42.121.237.23:8081",
"59.151.103.15:80",
"222.246.232.55:8101",
"218.203.13.185:80",
"111.40.194.48:80",
"222.74.28.14:23",
         ]

def get_proxies():
    if len(proxies)>0:
        import random
        index = random.randint(0, len(proxies)-1)
        return proxies[index]
    else:
        return ""
    
'''
新闻社评：韩福东， 米糕新闻日记， 洞见 
休闲旅行：周末做啥， 白菜价旅行 
八卦娱乐：绝对八卦
微信公众号
'''
    
sogou_urllib2 = None
weixin_urllib2 = None
sogou_count = 0
weixin_count = 0
    
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
依据块的定位符，从应答页面中分理出需要详细解析的结果块，可以有多块结果。
result：value
块名字：块数据
http://www.baidu.com/s?wd=github
return ["<a>oschina (开源中国) · </a>", "<a>首页、文档和下载 - 代码托管服务 - 开源中国社区</a>", ]
'''
def parse_block_match(page_src, start_str, end_str):
    block_data_map_list = []
    if start_str.strip()!="" or end_str.strip()!="":
        tmp_src = page_src.replace("\n","").replace("\r","")
        b_pos = tmp_src.find(start_str)
        block_num = 0
        while b_pos >= 0:
            block_num += 1
            e_pos = tmp_src.find(end_str,b_pos+len(start_str))
            block_data_map_list.append(tmp_src[b_pos+len(start_str):e_pos])
            if e_pos>=0:
                b_pos = tmp_src.find(start_str,e_pos)
            else: #未找到结束块e_pos为负值，跳出while循环
                b_pos = e_pos
    return block_data_map_list

'''
获得url请求数据的结果htmlsrc
url：请求链接
post_datas：post数据
url前缀做判断：如果是文件则读取文件内容返回，如果是文本内容则直接返回该内容，如果是url则返回该url应答页面的内容。
'''
def getUrlContent(url, post_datas={}, sleep_time=0, proxies={}, headers={}, urllib2=None):
    if len(url)==0:
        return ""
    url = urlzhuanyi(url)
    import random
    sleep_time = random.uniform(2,5)
    if sleep_time>0:
        time.sleep(sleep_time)
    if urllib2 is None:
        urllib2 = init_urllib2()
    
    if len(headers)==0:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-cn,zh;q=0.5",
            "Accept-Charset":"gb2312,utf-8;q=0.7,*;q=0.7",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            #"Cookie":"skin=noskin; path=/; domain=.amazon.com; expires=Wed, 25-Mar-2009 08:38:55 GMT\r\nsession-id-time=1238569200l; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT\r\nsession-id=175-6181358-2561013; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT"
        }
    req=urllib2.Request(url,headers=headers) #伪造request的header头，有些网站不支持，会拒绝请求;有些网站必须伪造header头才能访问
    htmlsrc = ""
    try:
        resp = None
        if post_datas:
            url_data = urllib.urlencode(post_datas)
            resp = urllib2.urlopen(req, url_data)
            print "request: "+str(url)+" , post_datas="+str(post_datas)
        else:
            resp = urllib2.urlopen(req)
            print "request: "+str(url)
        htmlsrc =resp.read()                
        code = resp.getcode()
        if code==200:
            response_headers = resp.headers.dict
            if response_headers.get("content-encoding")=="gzip":
                htmlsrc = gunzip(htmlsrc)
            elif response_headers.get("content-encoding") == "deflate":
                htmlsrc = deflate(htmlsrc)
        else:
            print "ERROR: code="+str(code)+" url="+url
    except:
        print "ERROR: request time out. url="+url,
        htmlsrc = ""

    return htmlsrc

def init_urllib2():
    cj = cookielib.CookieJar()
    if len(proxies)>0:
        proxy_support = urllib2.ProxyHandler(proxies)  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), HTTPRefererProcessor(), proxy_support, urllib2.HTTPHandler)
    else:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), HTTPRefererProcessor(), )
    urllib2.install_opener(opener)
    return urllib2

def gunzip(data):
    import gzip
    import StringIO
    data = StringIO.StringIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data

# zlib only provides the zlib compress format, not the deflate format;
def deflate(data):
    import zlib
    import StringIO
    data = StringIO.StringIO( data )
    try:               # so on top of all there's this workaround:
        gz = zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        gz = zlib.decompress(data)
    data = gz.read()
    gz.close()
    return data

'''
抓取搜狗页面
'''
def getSogouContent(url, post_datas={}, sleep_time=0, proxies={},):
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip,deflate,sdch",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        #"Cookie":"CXID=8F8A8A2502CBBED58ED24FE011474E44; SUID=1EC5E76561110C0A5332C67600095CA6; SUV=1396594719216119; ssuid=7214764425; pgv_pvi=7991477248; SMYUV=1403240797197204; usid=Q9hUBRtYFZ9TSfqY; IPLOC=CN3100; SNUID=28F3D250363039CA19695F1B3616C952; sct=10; ABTEST=8|1421655123|v17",
        "Host":"weixin.sogou.com",
        "Referer":"http://weixin.sogou.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
    }
    global sogou_urllib2
    if sogou_urllib2 is None:
        sogou_urllib2 = init_urllib2()
    htmlsrc = getUrlContent(url, post_datas, sleep_time, proxies, headers, sogou_urllib2)
    sogou_count = sogou_count+1
    print "sogou_count="+sogou_count
    return htmlsrc

'''
抓取微信页面
短时间内请求75次会被禁止IP，出现输入验证码页面
'''
def getWeixinContent(url, post_datas={}, sleep_time=0, proxies={},):
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip,deflate,sdch",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        #"Cookie":"isNarrow=0; ts_refer=www.baidu.com/s; ts_uid=8624891305; RK=ENGzloj0GQ; pgv_pvi=1479056384; ptui_loginuin=378823253; sd_userid=63491421117303085; sd_cookie_crttime=1421117303085; qzone_check=378823253_1421632062; pt2gguin=o0378823253; uin=o0378823253; skey=@bLNo4s8gl; ptisp=ctc; ptcz=fe4f9a22997c7bb50ff6c978cd1260f36f4f9af2e2f6d844c201083801254492; aboutVideo_v=0; pgv_info=ssid=s8831846406; pgv_pvid=1597739945; o_cookie=378823253; isVideo_DC=0",
        "Host":"mp.weixin.qq.com",
        #"If-Modified-Since":"Mon, 19 Jan 2015 08:27:42 GMT",
        "Referer":"http://weixin.sogou.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
    }
    global weixin_urllib2
    if weixin_urllib2 is None:
        weixin_urllib2 = init_urllib2()
    htmlsrc = getUrlContent(url, post_datas, sleep_time, proxies, headers, weixin_urllib2)
    weixin_count = weixin_count+1
    print "weixin_count="+weixin_count
    return htmlsrc

'''

'''
def gatherXici(url, post_datas={}, sleep_time=0, proxies={}, ):
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip,deflate,sdch",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Cookie":"visid_incap_257263=WdA97sejSUOxKdxzMstps2lvvFQAAAAAQUIPAAAAAAAtWRGx53uqfwqwQCbF1rbl; incap_ses_200_257263=R3CeOSixujh2eUEzbIvGAj6ZvFQAAAAAQWC7HzH3HM+tkphiyGYjVA==; _free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFRkkiJTIyNjgzODhmMWJkMjZjNGIxM2MwNWQ3Nzc5NzQyYWNmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMThLM1RBeUppdUhza056Mkl3TjBuNDQrY3E3cmt1Y2lhYjVjNUlUaTVaL2M9BjsARg%3D%3D--d820cc0f67f149a77b8d7864ddb9b42ab802f2ab; CNZZDATA4793016=cnzz_eid%3D240060596-1410663872-http%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1421644097",
        "Host":"www.xici.net.co",
        "If-None-Match":"a3ec5af5082fd11c95ea8a45745e052c",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
    }
    url = "http://www.xici.net.co/nn/"
    req=urllib2.Request(url,headers=headers)
    resp = urllib2.urlopen(req)
    #content = urllib2.urlopen('http://www.xici.net.co/nt/1').read() 
    print resp.read()
    print resp.headers.dict
    #htmlsrc = getUrlContent(url, post_datas, sleep_time, proxies, headers)
    return "htmlsrc"

if __name__ == "__main__":   
#     proxy = "183.207.232.193:8080"
#     page_src = getSogouContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page=1", proxies={"http":proxy})
#     print page_src
#     for item in range(100):
#         proxy = get_proxies()
#         print proxy
#         page_src = getSogouContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page=1&t=1421236929826", proxies={"http":proxy})
#         print len(page_src)
    #print getSogouContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page=1&t=1421236929826")
    #print getWeixinContent("http://mp.weixin.qq.com/s?__biz=MzA5NDI5ODczNA==&mid=206354655&idx=2&sn=b22f21b1d06b78955d722f53a26fbebc&3rd=MzA3MDU4NTYzMw==&scene=6#rd")
    #html = gatherXici("http://www.xici.net.co/nt/1")
    #print get_proxies()
#     page_src = getSogouContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page=1&t=1421236929826", {"http":proxies})
#     print len(page_src)
#     print page_src
    import random
    import time
    t= random.uniform(3,5)
    print t
    time.sleep(t)
    print t
    
    
