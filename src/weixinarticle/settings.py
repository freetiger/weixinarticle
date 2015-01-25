# -*- coding: utf-8 -*-
"""
Django settings for weixinarticle project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__)).replace('\\','/')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c%3(ca=@1uzs))3c@bji0loe$#$p67e#-wmfw_!ajtrk4%$%v@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',  #添加djcelery
    'xadmin',
    'crispy_forms',
    'reversion',
    'gather',
    'DjangoUeditor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'weixinarticle.urls'

WSGI_APPLICATION = 'weixinarticle.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'weixinarticle',
        'USER': 'root',
        'PASSWORD': '1161hyx',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TEMPLATE_DIRS = (
    BASE_DIR+'/weixinarticle/templates',
)

print TEMPLATE_DIRS

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'c:/weixinarticle_static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'c:/weixinarticle_media/'

#导入生产环境配置
#from gather.config import *

#缩略图配置
THUMBNAIL_SRC_ROOT = MEDIA_ROOT.join("thumbnail_src/")
THUMBNAIL_TGT_ROOT = MEDIA_ROOT.join("thumbnail_tgt/")
THUMBNAIL_WIDTH = 128
THUMBNAIL_HEIGHT = 128

#celery任务调度配置
# 配置djcelery相关参数，ResultStore默认存储在数据库可不必重写 ，
import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@0.0.0.0:5672//'
# BROKER_URL = 'redis://localhost:6379/0'
#任务定义所在的模块
CELERY_IMPORTS = ('gather.script', )
# 使用和Django一样的时区
CELERY_TIMEZONE = TIME_ZONE
 
#以上为基本配置，以下为周期性任务定义，以celerybeat_开头的  
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'add-every-1-minutes': {
        'task': 'gather.script.search_weixin_info',
        'schedule': timedelta(minutes=1)
    },
}
print "settings"


