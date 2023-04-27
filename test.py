
from pydantic import BaseModel
import jsonpickle

import json


class RouteMeta():
    title: str
    # icon: str | None = None
    # expended: bool | None = None
    # orderNo: int | None = None
    # hidden: bool | None = None
    # hiddenBreadcrumb: bool | None = None
    # single: bool | None = None
    # keepAlive: bool | None = None
    # frameSrc: str | None = None
    # frameBlank: bool | None = None

    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)



            
class RouteItem():
    path: str
    name: str
    # component: str | None = None
    # components: str | None = None
    # redirect: str | None = None
    # meta: RouteMeta
    # children: list | None = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

            
test = RouteItem(path='base', name='ListBase', component='/list/base/index', meta=RouteMeta(title='基础列表页'))
router_list = []
router_list.append(RouteItem(path='/list', name='list', component='LAYOUT', redirect='/list/base', meta=RouteMeta(title='哈哈哈哈哈', icon='view-list'), 
                                children=[RouteItem(path='base', name='ListBase', component='/list/base/index', meta=RouteMeta(title='基础列表页')), 
                                        RouteItem(path='card', name='ListCard', component='/list/card/index', meta=RouteMeta(title='卡片列表页')), 
                                        RouteItem(path='filter', name='ListFilter', component='/list/filter/index', meta=RouteMeta(title='筛选列表页')), 
                                        RouteItem(path='tree', name='ListTree', component='/list/tree/index', meta=RouteMeta(title='树状筛选列表页'))]))

encodejson = jsonpickle.encode(router_list[0], unpicklable=False)

print(encodejson)

print(json.loads(encodejson))
# print([i.__dict__ for i in router_list])
