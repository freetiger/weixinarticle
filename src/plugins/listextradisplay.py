# -*- coding: utf-8 -*-
'''
Created on 2015年1月16日

@author: heyuxing
'''
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
    
class ListExtraDisplayPlugin(BaseAdminPlugin):

    def get_list_queryset(self, queryset):
        print "queryset"
        print type(queryset)
        return queryset
    
    def get_result_list(self):
        result_list = super.list_queryset._clone()
        return result_list
    
site.register_plugin(ListExtraDisplayPlugin, ListAdminView)