# -*- coding: utf-8 -*-
'''
Created on 2015年1月14日
http://apscheduler.readthedocs.org/en/3.0/userguide.html
https://bitbucket.org/agronholm/apscheduler/src/e15559237256?at=master
@author: heyuxing
'''
from apscheduler.schedulers.background import BackgroundScheduler
from gather.models import WeixinInfo
from gather.script import scan_article, dbutils
import datetime
import time
import logging
logging.basicConfig()

def scan_all_article():
    weixinInfoList = dbutils.getWeixinInfoList()
    for weixinInfo in weixinInfoList:
        scan_article(weixin_info_id=weixinInfo.id)
        
def scheduler_scan_all_article():
    print "scheduler_scan_all_article is start!"
    #定时任务启动
    scheduler = BackgroundScheduler()
    scheduler.add_job(scan_all_article, 'cron', hour='0-23', minute=50)
    scheduler.start()
    
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  


def say_hello():
    print "Hello World:"+str(datetime.datetime.now())


if __name__ == '__main__':
    scan_all_article()
    #scheduler_scan_all_article()
#     #定时任务启动
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(say_hello, 'cron', hour='0-23', minute=30)
#     scheduler.start()
#     
#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible



