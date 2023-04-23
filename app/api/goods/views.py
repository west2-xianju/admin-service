from flask import request
from . import goods
from .models import Good
from sqlalchemy import and_
from sqlalchemy.sql import text

from ...models import BaseResponse
from flask_jwt_extended import jwt_required
import json


@goods.route('/', methods=['GET'])
@jwt_required()
def get_goods_list():
    filter_condition = set()
    filter_condition.add(Good.game.like('%' + request.args.get('game') + '%'))
    filter_condition.add(Good.title.like(
        '%' + request.args.get('title') + '%'))
    filter_condition.add(Good.detail.like(
        '%' + request.args.get('detail') + '%'))

    if request.args.get('good_id'):
        filter_condition.add(Good.good_id == request.args.get('good_id'))

    if request.args.get('seller_id'):
        filter_condition.add(Good.seller_id == request.args.get('seller_id'))

    order = request.args.get('order_by')
    order_map = ['dec', 'asc']
    if request.args.get('order') in order_map:
        order = request.args.get('order') + order

    query_result = Good.query.order_by(text(order)).filter(and_(*filter_condition)).paginate(
        page=request.args.get('page', 1, type=int), per_page=request.args.get('per_page', 10, type=int)).items

    return BaseResponse(data={'goods': [i.to_dict() for i in query_result]}).dict()


@goods.route('/<int:good_id>', methods=['GET'])
@jwt_required()
def get_good_info(good_id):
    good_info = Good.query.filter_by(good_id=good_id).first()

    if not good_info:
        return BaseResponse(code=404, message='good not found').dict()

    return BaseResponse(data=good_info.to_dict()).dict()


@goods.route('/<int:good_id>', methods=['PUT'])
@jwt_required()
def modify_good_info(good_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()

    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
        
    data = json.loads(request.data)

    Good.query.filter_by(good_id=good_id).update(data)

    return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()


@goods.route('/<int:good_id>', methods=['DELETE'])
@jwt_required()
def delete_good(good_id):
    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    result = Good.query.filter_by(good_id=good_id).delete()

    return BaseResponse(data={'delete_count': result}).dict()


@goods.route('/<int:good_id>', methods=['PATCH'])
@jwt_required()
def hide_good(good_id):
    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    Good.query.filter_by(good_id=good_id).update({'state': 'pending'})

    return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()


@goods.route('/<int:good_id>/censor', methods=['PATCH'])
@jwt_required()
def censor_good(good_id):
    if not Good.query.filter_by(good_id=good_id).first():
        return BaseResponse(code=404, message='good not found').dict()

    data = json.loads(request.data)

    if data.get('op') not in ['allow', 'reject']:
        return BaseResponse(code=400, message='op must be allow or reject').dict()

    STATE_MAP = {'allow': 'released', 'reject': 'locked'}
    Good.query.filter_by(good_id=good_id).update(
        {'state': STATE_MAP[data.get('op')]})

    return BaseResponse(data=Good.query.filter_by(good_id=good_id).first().to_dict()).dict()


@goods.route('/', methods=['POST'])
@jwt_required()
def add_good():
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()

    result = Good().from_dict(json.loads(request.data))

    return BaseResponse(data=result.to_dict()).dict()
