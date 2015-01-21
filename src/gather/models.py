# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''
from django.db import models

class ImportWeixinInfo(models.Model):
    weixin_names = models.TextField(verbose_name='微信名，每一行一个')
    num = models.IntegerField(default=0, verbose_name='微信号数目')
    is_all = models.BooleanField(default=False, verbose_name='全部（默认最多十个）')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')   
    
    def __unicode__(self):
        return self.weixin_names  
    
    def save(self):
        super(ImportWeixinInfo, self).save()
        #
        from gather.script import search_weixin_info
        weixin_name_list = self.weixin_names.splitlines()
        for weixin_name in weixin_name_list:
            weixin_infos = search_weixin_info(weixin_name, self.is_all)
            for weixin_info in weixin_infos:
                filterWeixinInfo = FilterWeixinInfo()
                filterWeixinInfo.import_weixin_info_id = self.pk
                filterWeixinInfo.keyword = weixin_name
                filterWeixinInfo.weixin_name = weixin_info[0]
                filterWeixinInfo.weixin_no = weixin_info[1]
                filterWeixinInfo.openid = weixin_info[2]
                filterWeixinInfo.save()
                self.num = self.num+1
        #
        super(ImportWeixinInfo, self).save()
    
    class Meta:
        ordering = ['-create_date']
        verbose_name='导入微信' 
        verbose_name_plural='导入微信'

class FilterWeixinInfo(models.Model):
    import_weixin_info = models.ForeignKey(ImportWeixinInfo, verbose_name='导入关键字')
    keyword = models.TextField(verbose_name='搜索关键字')
    weixin_name = models.CharField(blank=True, null=True, max_length=256, verbose_name='微信名')
    weixin_no = models.CharField(blank=True, null=True, max_length=256, verbose_name='微信号')
    openid = models.CharField(blank=True, null=True, max_length=256, verbose_name='微信openid')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')     
    
    class Meta:
        ordering = ['-create_date']
        verbose_name='筛选微信' 
        verbose_name_plural='筛选微信'
        
        
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
    weixin_name = models.CharField(max_length=256, verbose_name='微信名')
    openid = models.CharField(max_length=256, verbose_name='微信openid')
    weixin_no = models.CharField(blank=True, max_length=256, verbose_name='微信号')
    title = models.CharField(max_length=256, verbose_name='文章标题')
    url = models.CharField(max_length=1024, verbose_name='文章源URL')
    content = models.TextField(verbose_name='文章内容')
    publish_date = models.DateField(verbose_name='发布日期')
    thumbnail_url = models.CharField(max_length=1024, verbose_name='缩略图源URL')
    thumbnail_path = models.CharField(max_length=1024, verbose_name='缩略图服务器路径')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    
    def __unicode__(self):
        return str(self.weixin_info)+": "+self.title
    
    class Meta:
        ordering = ['-create_date']
        verbose_name='微信文章' 
        verbose_name_plural='微信文章'
        
        
    
    