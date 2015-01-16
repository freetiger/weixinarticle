# -*- coding: utf-8 -*-
'''
Created on 2014年12月31日

@author: Administrator
'''
from django.utils.importlib import import_module
import xadmin
from xadmin.views.base import CommAdminView

from gather.models import FilterWeixinInfo, ImportWeixinInfo, WeixinInfo, WeixinArticle


# from xadmin.plugins.inline import Inline
class GolbeSetting(object):
    # 设置主题可选择  
    enable_themes= True 
    use_bootswatch = True 
    # 设置系统标题  
    site_title='微信文章抓取系统' 
    site_footer  = '微信文章抓取系统'
    
#     reversion_enable = True

    # 设置菜单风格, 叠加起来  
    #menu_style = 'accordion' 
    apps_label_title = {  
           'gather':u'微信数据',
           'auth':u'用户权限',
           'reversion':u'操作记录',
    }  
    globe_search_models = [WeixinInfo, WeixinArticle]
    
xadmin.site.register(CommAdminView, GolbeSetting)

class BaseAdmin(object):
    #导出
    list_export = ()
    list_export_fixed = ('xlsx', 'xls', 'csv', 'xml', 'json')
    #数据版本控制，默认记录10个版本，可以调整。恢复删除的数据
    reversion_enable = True
    #相关模块操作
    use_related_menu=False
 
#微信列表
class ImportWeixinInfoAdmin(BaseAdmin):
    list_display = ('weixin_names', 'create_date', )
       
#微信列表
class FilterWeixinInfoAdmin(BaseAdmin):
    list_display = ('keyword', 'weixin_name', 'weixin_no', 'openid', 'create_date', )
    #设置搜索框和其模糊搜索的范围
    search_fields = ('keyword', 'weixin_name', 'weixin_no', 'openid',) 
    list_editable = ('weixin_name', 'weixin_no', 'openid',  )
    
#微信列表
class WeixinInfoAdmin(BaseAdmin):
    list_display = ('weixin_name', 'weixin_no', 'openid', 'last_scan_date', 'update_num', 'create_date', )
    #设置搜索框和其模糊搜索的范围
    search_fields = ('weixin_name', 'weixin_no', 'openid',) 
    list_editable = ('weixin_name', 'weixin_no', 'openid',  )
    #操作列表
    list_operate=['<a href="/gather/scan_article/{{pk}}/" target="_blank">执行</a>'
                  , '<a href="/gather/weixinarticle/?_p_weixin_info__id__exact={{pk}}">文章列表</a>', ]
    
    def get_list_queryset(self):
        queryset = super(WeixinInfoAdmin, self).get_list_queryset()
        print queryset,type(queryset),type(queryset[0])
        return queryset
#         for item in queryset:
#             print item.weixin_name
#             item.weixin_name="heyuxing"
#         for item in queryset:
#             print item.weixin_name
# #         if len(queryset)==0:
# #             from gather.script import search_weixin_info
# #             weixin_infos = search_weixin_info("")
# #             for weixin_info in weixin_infos:
# #                 weixinInfo = WeixinInfo()
# #                 weixinInfo.weixin_name = weixin_info[0]
# #                 weixinInfo.weixin_no = weixin_info[1]
# #                 weixinInfo.openid = weixin_info[2]
# #                 queryset.append(weixinInfo)
# #             print weixin_infos
#         return queryset

#微信列表
class WeixinArticleAdmin(BaseAdmin):
    list_display = ('weixin_info', 'title', 'create_date', )
    #设置搜索框和其模糊搜索的范围
    search_fields = ('weixin_info.weixin_name', 'weixin_info.weixin_no', 'weixin_info.openid','title' ) 
    list_editable = ('title', )
    #操作列表
    list_operate=['<a href="/gather/article_show/{{pk}}/" target="_blank">查看文章</a>', ]

xadmin.site.register(FilterWeixinInfo, FilterWeixinInfoAdmin)
xadmin.site.register(ImportWeixinInfo, ImportWeixinInfoAdmin)
xadmin.site.register(WeixinInfo, WeixinInfoAdmin)
xadmin.site.register(WeixinArticle, WeixinArticleAdmin)

#自定义插件导入   
import_module('plugins.operatelist')
import_module('plugins.export')
# import_module('plugins.listextradisplay')

