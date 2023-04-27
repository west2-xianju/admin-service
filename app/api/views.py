from flask import request
from . import api
from .models import RouteItem, RouteMeta
import jsonpickle

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json

@api.route('/menu', methods=['GET'])
def get_menu_list():
    router_list = []
    router_list.append(RouteItem(path='/list', name='list', component='LAYOUT', redirect='/list/base', meta=RouteMeta(title='test pages', icon='view-list'), 
                                    children=[RouteItem(path='base', name='ListBase', component='/list/base/index', meta=RouteMeta(title='基础列表页')), 
                                            RouteItem(path='card', name='ListCard', component='/list/card/index', meta=RouteMeta(title='卡片列表页')), 
                                            RouteItem(path='filter', name='ListFilter', component='/list/filter/index', meta=RouteMeta(title='筛选列表页')), 
                                            RouteItem(path='tree', name='ListTree', component='/list/tree/index', meta=RouteMeta(title='树状筛选列表页'))]))
    router_list.append(RouteItem(path='/censor', name='censor', component='LAYOUT', meta=RouteMeta(title='审核管理', icon='user-talk'), 
                                 children=[RouteItem(path='good', name='CensorGood', component='/censor/good/index', meta=RouteMeta(title='货物审核')), 
                                           RouteItem(path='user', name='CensorUser', component='/censor/user/index', meta=RouteMeta(title='用户审核'))]))
    router_list.append(RouteItem(path='/app', name='app', component='LAYOUT', meta=RouteMeta(title='业务管理', icon='app'),
                                 children=[RouteItem(path='user', name='AppUser', component='/app/user/index', meta=RouteMeta(title='用户管理')),
                                           RouteItem(path='good', name='AppGood', component='/app/good/index', meta=RouteMeta(title='货物管理')),
                                           RouteItem(path='issue', name='AppIssue', component='/app/issue/index', meta=RouteMeta(title='纠纷管理'))]))
    router_list.append(RouteItem(path='/payment', name='payment', component='LAYOUT', meta=RouteMeta(title='支付管理', icon='money-circle'),
                                 children=[RouteItem(path='wallet', name='PaymentWallet', component='/payment/wallet/index', meta=RouteMeta(title='钱包管理')),
                                           RouteItem(path='order', name='PaymentOrder', component='/payment/order/index', meta=RouteMeta(title='订单管理')),
                                           RouteItem(path='system', name='PaymentSystem', component='/payment/system/index', meta=RouteMeta(title='系统管理'))]))
    # router_list.append(RouteItem(path='/admin', name='admin', component='LAYOUT', meta=RouteMeta(title='系统管理', icon='setting'),
    #                              children=[RouteItem(path='user', name='AdminUser', component='/admin/user/index', meta=RouteMeta(title='用户管理')),
    #                                        RouteItem(paht='log', name='AdminLog', component='/admin/log/index', meta=RouteMeta(title='日志管理')),
    #                                        RouteItem(path='setting', name='AdminSetting', component='/admin/setting/index', meta=RouteMeta(title='系统设置'))]))
    
    router_list.append(RouteItem(path='/setting', name='setting', component='LAYOUT', meta=RouteMeta(title='系统设置', icon='setting'),
                                 children=[RouteItem(path='admin', name='SettingAdmin', component='/setting/admin/index', meta=RouteMeta(title='管理员设置')),
                                           RouteItem(path='log', name='SettingLog', component='setting/log/index', meta=RouteMeta(title='日志管理'))]))

    # return json.loads(router_json)
    return BaseResponse(data={'list':  [json.loads(jsonpickle.encode(i, unpicklable=False)) for i in router_list]}).dict()
