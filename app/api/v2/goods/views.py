from flask import request
from . import goods
from .models import Good
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json
from datetime import datetime

from .schemas import UpdateGoodForm, CreateGoodForm

from flask_restful import Resource, Api

goodsApi = Api(goods)

class Goods(Resource):
    __decorators__ = [jwt_required()]
    
    def get(self, good_id):
        good_info = Good.query.filter_by(good_id=good_id).first()

        if not good_info:
            return BaseResponse(code=404, message='good not found').dict()

        return BaseResponse(data=good_info.to_dict()).dict()

    def put(self, good_id):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()

        if not Good.query.filter_by(good_id=good_id).first():
            return BaseResponse(code=404, message='good not found').dict()

        if not request.data:
            return BaseResponse(code=400, message='request data is empty').dict()

        data = json.loads(request.data)
        
        if data['state']:
            data['state'] = Good.GOOD_STATES_ENUM[Good.GOOD_STATES_ENUM_DESCRIPTION.index(data['state'])]

        updateForm = UpdateGoodForm(**data)
        Good.query.filter_by(good_id=good_id).update(dict(updateForm))

        return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()
    def delete(self, good_id):
        if not Good.query.filter_by(good_id=good_id).first():
            return BaseResponse(code=404, message='good not found').dict()

        result = Good.query.filter_by(good_id=good_id).delete()

        return BaseResponse(data={'delete_count': result}).dict()
    def patch(self, good_id):
        if not Good.query.filter_by(good_id=good_id).first():
            return BaseResponse(code=404, message='good not found').dict()

        Good.query.filter_by(good_id=good_id).update({'state': Good.GOOD_STATES_ENUM[0]})

        return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()

class GoodsList(Resource):
    method_decorators = [jwt_required()]
    def get(self):
        filter_condition = set()
        filter_condition.add(Good.game.like('%' + request.args.get('game', '', type=str) + '%'))
        filter_condition.add(Good.title.like('%' + request.args.get('title', '', type=str) + '%'))
        filter_condition.add(Good.detail.like('%' + request.args.get('detail', '', type=str) + '%'))
        if request.args.get('state', '', type=str).lower() in Good.GOOD_STATES_ENUM_DESCRIPTION:
            state = Good.GOOD_STATES_ENUM_DESCRIPTION.index(request.args.get('state', '', type=str).lower())
            filter_condition.add(Good.state == Good.GOOD_STATES_ENUM[state])

        if request.args.get('uid'):
            filter_condition.add(Good.good_id == request.args.get('uid', type=int))

        if request.args.get('seller_id'):
            filter_condition.add(Good.seller_id == request.args.get('seller_id'))

        order_by = request.args.get('order_by', '', type=str)
        order_list = ['asc', 'desc']
        if request.args.get('order', '') in order_list:
            order_by = order_by + ' ' + request.args.get('order', '')

        query_result = Good.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(
            page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 10, type=int))
        
        # return BaseResponse().dict()

        return BaseResponse(data={'goods': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()
    def post(self):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()

        data = json.loads(request.data)
        createForm = CreateGoodForm(**data)
        createForm.state = Good.GOOD_STATES_ENUM[Good.GOOD_STATES_ENUM_DESCRIPTION.index(createForm.state)]
        result = Good().from_dict(dict(createForm))

        return BaseResponse(data=result.to_dict()).dict()


goodsApi.add_resource(Goods, '/<int:good_id>')
goodsApi.add_resource(GoodsList, '/')


@goods.route('/<int:good_id>/censor', methods=['PATCH'])
@jwt_required()
def censor_good(good_id):
    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    data = json.loads(request.data)
    print(data.get('op'))

    if data.get('op') not in ['allow', 'reject']:
        return BaseResponse(code=400, message='op must be allow or reject').dict()

    STATE_MAP = {'allow': 'released', 'reject': 'locked'}
    Good.query.filter_by(good_id=good_id).update(
        {'state': Good.GOOD_STATES_ENUM[Good.GOOD_STATES_ENUM_DESCRIPTION.index(STATE_MAP[data.get('op')])], 'publish_time': datetime.utcnow()})

    return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()

@goods.route('/stats', methods=['GET'])
@jwt_required()
def get_good_stats():
    released_goods_count = len(Good.query.filter_by(state=Good.GOOD_STATES_ENUM[1]).all())
    total_goods_count = len(Good.query.all())
    
    ret_info = [{'value': total_goods_count-released_goods_count, 'name': '未上架'}, {'value': released_goods_count, 'name': '已上架'}]
    
    return BaseResponse(data={'stat': ret_info}).dict()