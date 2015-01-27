# -*- coding: utf-8 -*-
'''
Created on 2015年1月23日

@author: heyuxing
'''
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weixinarticle.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()