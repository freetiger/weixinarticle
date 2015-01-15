# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''
from django.db import models


class WeixinInfo(models.Model):
    weixin_name = models.CharField(max_length=256, verbose_name='微信名')
    weixin_no = models.CharField(blank=True, max_length=256, verbose_name='微信号')
    openid = models.CharField(max_length=256, verbose_name='微信openid')
    last_scan_date = models.DateTimeField(blank=True, null=True, verbose_name='最近扫描时间')     
    update_num = models.IntegerField(default=0, verbose_name='更新文章数')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')     
    
    def __unicode__(self):
        return self.weixin_name
    
    class Meta:
        ordering = ['-create_date']
        verbose_name='微信列表' 
        verbose_name_plural='微信列表'
        
class WeixinArticle(models.Model):
    weixin_info = models.ForeignKey(WeixinInfo, verbose_name='微信号信息')
    title = models.CharField(max_length=256, verbose_name='文章标题')
    url = models.CharField(max_length=1024, verbose_name='文章源URL')
    content = models.TextField(verbose_name='文章内容')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    
    def __unicode__(self):
        return str(self.weixin_info)+": "+self.title
    
    class Meta:
        ordering = ['-create_date']
        verbose_name='微信文章' 
        verbose_name_plural='微信文章'
        
        
    
    