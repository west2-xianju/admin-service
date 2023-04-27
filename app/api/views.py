from flask import request
from . import api
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json


@api.route('/menu', methods=['GET'])
def get_menu_list():
    router_json = '''{
	"code": 0,
	"data": {
		"list": [{
			"children": [{
				"component": "/list/base/index",
				"meta": {
					"title": "基础列表页"
				},
				"name": "ListBase",
				"path": "base"
			}, {
				"component": "/list/card/index",
				"meta": {
					"title": "卡片列表页"
				},
				"name": "ListCard",
				"path": "card"
			}, {
				"component": "/list/filter/index",
				"meta": {
					"title": "筛选列表页"
				},
				"name": "ListFilter",
				"path": "filter"
			}, {
				"component": "/list/tree/index",
				"meta": {
					"title": "树状筛选列表页"
				},
				"name": "ListTree",
				"path": "tree"
			}],
			"component": "LAYOUT",
			"meta": {
				"icon": "view-list",
				"title": "哈哈哈哈哈"
			},
			"name": "list",
			"path": "/list",
			"redirect": "/list/base"
		}]
	}
}'''
    router = json.loads(router_json)
    return router
