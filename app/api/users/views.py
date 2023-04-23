from flask import request
from . import users
from .models import Good
from sqlalchemy import and_
from sqlalchemy.sql import text

from ...models import BaseResponse
from flask_jwt_extended import jwt_required
import json

@users.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_info(user_id):
    user_info = Good.query.filter_by(user_id=user_id).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    return BaseResponse(data=user_info.to_dict()).dict()


@users.route('/', methods=['GET'])
@jwt_required()
def get_user_list():
    filter_condition = set()
    # print(request.args.to_dict())
    filter_condition.add(Good.username.like('%' + request.args.get('username') + '%'))
    filter_condition.add(Good.nickname.like('%' + request.args.get('nickname') + '%'))
    filter_condition.add(Good.email.like('%' + request.args.get('email') + '%'))
    filter_condition.add(Good.realname.like('%' + request.args.get('realname') + '%'))
    filter_condition.add(Good.id_number.like('%' + request.args.get('id_number') + '%'))
    if request.args.get('user_id'):
        filter_condition.add(Good.user_id == request.args.get('user_id'))
     
    order = request.args.get('order_by')
    order_map = ['dec', 'asc']
    if request.args.get('order') in order_map:
        order = request.args.get('order') + order
        
    
    query_result = Good.query.order_by(text(order)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('per_page', 10, type=int)).items
    
    return BaseResponse(data={'users': [i.to_dict() for i in query_result]}).dict()



# add a new user
@users.route('/', methods=['POST'])
@jwt_required()
def add_user():
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    data = json.loads(request.data)
    if Good.query.filter_by(username=data['username']).first():
        return BaseResponse(code=400, message='username already exists').dict()
    if Good.query.filter_by(email=data['email']).first():
        return BaseResponse(code=400, message='email already exists').dict()
    
    new_user = Good().from_dict(data).save()
    
    return BaseResponse(data=new_user.to_dict()).dict()


# modify user info
@users.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def modify_user(user_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    data = json.loads(request.data)
    if not Good.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    from .models import hash_and_salt_password
    hashed_password = hash_and_salt_password(data['password'])
    data.update({'password': hashed_password})
    
    Good.query.filter_by(user_id=user_id).update(dict(data))
    
    return BaseResponse(data = Good.query.filter_by(user_id=user_id).first().to_dict()).dict()


# change user authority
@users.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def block_user(user_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not Good.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    try:
        data = json.loads(request.data)
    except:
        return BaseResponse(code=400, message='invalid json').dict()
    
    
    if data['blocked'] not in [True, False]:
        return BaseResponse(code=400, message='blocked must be true or false').dict()
    
    Good.query.filter_by(user_id=user_id).update({'blocked': data['blocked']})
    
    return BaseResponse(data = Good.query.filter_by(user_id=user_id).first().to_dict()).dict()


# delete user
@users.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not Good.query.filter_by(user_id=user_id).first():
        return BaseResponse(code=404, message='user not found').dict()
    
    user = Good.query.filter_by(user_id=user_id).first()
    Good.query.filter_by(user_id=user_id).first().delete()
    
    return BaseResponse(data=user.to_dict()).dict()