# -*- coding: utf-8 -*-
'''
Created on 2015年1月25日

@author: heyuxing
'''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*', ]
    
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'nidongde',
        'USER': 'root',
        'PASSWORD': 'nidongde',
    }
}
    
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/webapps/weixinarticle_static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/webapps/weixinarticle_media/'
    
    
    