# -*- coding: utf-8 -*-
'''
Created on 2015年1月14日
http://apscheduler.readthedocs.org/en/3.0/userguide.html
https://bitbucket.org/agronholm/apscheduler/src/e15559237256?at=master
@author: heyuxing
'''
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
import logging
logging.basicConfig()


def say_hello():
    print "Hello World:"+str(datetime.datetime.now())


if __name__ == '__main__':
    #定时任务启动
    scheduler = BackgroundScheduler()
    scheduler.add_job(say_hello, 'cron', hour='0-23', second=3)
    scheduler.start()
    
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible



