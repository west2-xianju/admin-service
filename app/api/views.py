from flask import request
from . import api
from .models import RouteItem, RouteMeta
import jsonpickle

from ..models import BaseResponse
from .users.models import User
from .goods.models import Good
from .issues.models import Issue
from .wallets.models import Wallet
from flask_jwt_extended import jwt_required
import json, requests

from datetime import datetime
start_time = datetime.utcnow()

@api.route('/menu', methods=['GET'])
def get_menu_list():
    router_list = []
    router_list.append(RouteItem(path='/censor', name='censor', component='LAYOUT', meta=RouteMeta(title='审核管理', icon='user-talk'), 
                                 children=[RouteItem(path='good', name='CensorGood', component='/censor/good/index', meta=RouteMeta(title='货物审核')), 
                                           RouteItem(path='user', name='CensorUser', component='/censor/user/index', meta=RouteMeta(title='用户审核'))]))
    router_list.append(RouteItem(path='/app', name='app', component='LAYOUT', meta=RouteMeta(title='业务管理', icon='app'),
                                 children=[RouteItem(path='user', name='AppUser', component='/app/user/index', meta=RouteMeta(title='用户管理')),
                                           RouteItem(path='user/create', name='AppCreateUser', component='/app/user/createForm/index', meta=RouteMeta(title='创建用户', hidden=True)),
                                           RouteItem(path='good', name='AppGood', component='/app/good/index', meta=RouteMeta(title='货物管理')),
                                           RouteItem(path='issue', name='AppIssue', component='/app/issue/index', meta=RouteMeta(title='纠纷管理'))]))
    router_list.append(RouteItem(path='/payment', name='payment', component='LAYOUT', meta=RouteMeta(title='支付管理', icon='money-circle'),
                                 children=[RouteItem(path='wallet', name='PaymentWallet', component='/payment/wallet/index', meta=RouteMeta(title='钱包管理')),
                                           RouteItem(path='order', name='PaymentOrder', component='/payment/order/index', meta=RouteMeta(title='订单管理')),
                                           RouteItem(path='system', name='PaymentSystem', component='/payment/system/index', meta=RouteMeta(title='系统管理'))]))
    
    
    router_list.append(RouteItem(path='/list', name='list', component='LAYOUT', redirect='/list/base', meta=RouteMeta(title='test pages', icon='view-list'), 
                                    children=[RouteItem(path='base', name='ListBase', component='/list/base/index', meta=RouteMeta(title='基础列表页')), 
                                            RouteItem(path='card', name='ListCard', component='/list/card/index', meta=RouteMeta(title='卡片列表页')), 
                                            RouteItem(path='filter', name='ListFilter', component='/list/filter/index', meta=RouteMeta(title='筛选列表页')), 
                                            RouteItem(path='tree', name='ListTree', component='/list/tree/index', meta=RouteMeta(title='树状筛选列表页')),
                                            RouteItem(path='test', name='Test', component='/testpage', meta=RouteMeta(title='测试页面'))]))
    # router_list.append(RouteItem(path='/admin', name='admin', component='LAYOUT', meta=RouteMeta(title='系统管理', icon='setting'),
    #                              children=[RouteItem(path='user', name='AdminUser', component='/admin/user/index', meta=RouteMeta(title='用户管理')),
    #                                        RouteItem(paht='log', name='AdminLog', component='/admin/log/index', meta=RouteMeta(title='日志管理')),
    #                                        RouteItem(path='setting', name='AdminSetting', component='/admin/setting/index', meta=RouteMeta(title='系统设置'))]))
    
    router_list.append(RouteItem(path='/setting', name='setting', component='LAYOUT', meta=RouteMeta(title='系统设置', icon='setting'),
                                 children=[RouteItem(path='admin', name='SettingAdmin', component='/setting/admin/index', meta=RouteMeta(title='管理员设置')),
                                           RouteItem(path='log', name='SettingLog', component='setting/log/index', meta=RouteMeta(title='日志管理'))]))

    # return json.loads(router_json)
    return BaseResponse(data={'list':  [json.loads(jsonpickle.encode(i, unpicklable=False)) for i in router_list]}).dict()

# export interface DashboardPanel {
#   title: string;
#   number: string | number;
#   leftType: string;
#   upTrend?: string;
#   downTrend?: string;
# }

class DashboardPanel:
    title: str
    number: str
    leftType: str
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@api.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_info():
    # to-do
    # redis to cache last period data then calculate the increasing/decreasing rating.
    
    # user_count = User.query.count()
    # user_online = 1
    # good_count = Good.query.count()
    # good_pending = Good.query.filter_by(state=Good.GOOD_STATES_ENUM[0]).count()
    # issue_count = Issue.query.count()
    # sys_start_time = start_time
    url = "http://localhost:5000/dev/chat"
    response = requests.request("GET", url)
    user_online = response.json()['code']
    print(user_online)
    
    DashboardPanelList = []
    DashboardPanelList.append(DashboardPanel(title='用户总数', number=User.query.count(), leftType='icon-user', route='/app/user'))
    DashboardPanelList.append(DashboardPanel(title='在线用户', number=user_online, leftType='icon-bar'))
    DashboardPanelList.append(DashboardPanel(title='货物总数', number=Good.query.count(), leftType='icon-control-platform', route='/app/good'))
    DashboardPanelList.append(DashboardPanel(title='待审核货物', number=Good.query.filter_by(state=Good.GOOD_STATES_ENUM[0]).count(), leftType='icon-layers', route='/censor/good'))
    # DashboardPanelList.append(DashboardPanel(title='纠纷总数', number=Issue.query.count(), leftType='issue'))
    # DashboardPanelList.append(DashboardPanel(title='系统启动时间', number=start_time, leftType='time'))
    
    for _ in DashboardPanelList:
        print(jsonpickle.encode(_, unpicklable=False))
    return BaseResponse(data={'list':  json.loads(jsonpickle.encode(DashboardPanelList, unpicklable=False))}).dict()