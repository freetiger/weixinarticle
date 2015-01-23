# -*- coding: utf-8 -*-
'''
Created on 2015年1月23日

@author: heyuxing
'''
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weixinarticle.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()