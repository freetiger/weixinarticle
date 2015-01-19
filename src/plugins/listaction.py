# -*- coding: utf-8 -*-
'''
Created on 2015��1��17��

@author: Administrator
'''
from xadmin.plugins.actions import BaseActionView

from gather.models import WeixinInfo
from gather.dbutils import getWeixinInfoList
class AddWeixinNoAction(BaseActionView):

    # 这里需要填写三个属性
    action_name = "add_weixin_no_action"    #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = "添加微信号" #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.

    model_perm = 'delete'    #: 该 Action 所需权限 delete change

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        for obj in queryset:
            # obj 的操作
            weixinInfoList=[]
            if obj.weixin_no is not None:
                weixinInfoList.extend(getWeixinInfoList(weixin_no=obj.weixin_no))
            if obj.openid is not None:
                weixinInfoList.extend(getWeixinInfoList(openid=obj.openid))
            if len(weixinInfoList)==0:
                weixinInfo = WeixinInfo()
                weixinInfo.weixin_name = obj.weixin_name
                weixinInfo.weixin_no = obj.weixin_no
                weixinInfo.openid = obj.openid
                weixinInfo.save()
            obj.delete()
        # 返回 HttpResponse
        #return HttpResponse(...)
