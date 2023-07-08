from flask import request
from . import users
from .models import User
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

from ..goods.models import Good
from .schemas import UpdateUserForm

from flask_restful import Resource, Api

userApi = Api(users)

class Users(Resource):
    method_decorators = [jwt_required()]
    def get(self, user_id):
        # Find the user info from the database
        user_info = User.query.filter_by(user_id=user_id).first()

        # If the user isn't found, return a 404 error
        if not user_info:
            return BaseResponse(code=404, message='user not found').dict()

        # Return the user info as a JSON object
        return BaseResponse(data=user_info.to_dict()).dict()

    
    def put(self, user_id):
        # Make sure that the request has the correct content type
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()

        # Make sure that the user exists
        if not User.query.filter_by(user_id=user_id).first():
            return BaseResponse(code=404, message='user not found').dict()

        # Make sure that the request data is not empty
        if not request.data:
            return BaseResponse(code=400, message='request data is empty').dict()

        # Parse the request data into a dictionary
        data = json.loads(request.data)
        updateData = UpdateUserForm(**data)
        
        # Get the user object from the database
        userObject = User.query.filter_by(user_id=user_id).first()
        
        # If the request data includes a password, then set the user object's password to the new value
        if data.get('password'):
            userObject.password = data['password']

        # Update the user in the database
        User.query.filter_by(user_id=user_id).update(dict(updateData))

        # Return the updated user
        return BaseResponse(data=User.query.filter_by(user_id=user_id).first().to_dict()).dict()
    
    def patch(self, user_id):
        # check if user_id is provided
        if not user_id:
            return BaseResponse(code=400, message='user_id is required').dict()
        # check if user_id exists
        if not User.query.filter_by(user_id=user_id).first():
            return BaseResponse(code=404, message='user not found').dict()
        
        # check if blocked is provided
        if request.json.get('blocked') not in [True, False]:
            return BaseResponse(code=400, message='blocked must be true or false').dict()
        
        # update blocked
        User.query.filter_by(user_id=user_id).update({'blocked': request.json.get('blocked')})
        
        if request.json.get('blocked') == True:
            # check if goods exist
            goods_list = Good.query.filter_by(seller_id=user_id, state='released').all()
            for _ in goods_list:
                 _.state = 'locked'
        
        return BaseResponse(data=User.query.filter_by(user_id=user_id).first().to_dict()).dict()
    
    def delete(self, user_id):
        if not User.query.filter_by(user_id=user_id).first():
            return BaseResponse(code=404, message='user not found').dict()

        result = User.query.filter_by(user_id=user_id).delete()

        return BaseResponse(data={'delete_count': result}).dict()
    
class UsersList(Resource):
    method_decorators = [jwt_required()]
    def get(self):
        filter_condition = set()
        filter_condition.add(User._username.like('%' + request.args.get('username', '', type=str) + '%'))
        filter_condition.add(User.nickname.like('%' + request.args.get('nickname', '', type=str) + '%'))
        filter_condition.add(User._email.like('%' + request.args.get('email', '', type=str) + '%'))
        if request.args.get('realname', None, type=str):
            filter_condition.add(User.realname.like('%' + request.args.get('realname', '', type=str) + '%'))
        if request.args.get('id_number', None, type=str):
            filter_condition.add(User.id_number.like('%' + request.args.get('id_number', '', type=str) + '%'))
        if request.args.get('blocked', '', type=str).lower() in ['true', 'false']:
            filter_condition.add(User.blocked == (request.args.get('blocked', '', type=str).lower() == 'true'))
        if request.args.get('uid'):
            filter_condition.add(User.user_id == request.args.get('uid'))
        if request.args.get('start', None, type=str):
            filter_condition.add(User.register_time >= request.args.get('start', None, type=str))
        if request.args.get('end', None, type=str):
            filter_condition.add(User.register_time <= request.args.get('end', None, type=str))
        
        order_by = request.args.get('order_by', '', type=str)
        order_list = ['asc', 'desc']
        if request.args.get('order') in order_list:
            order_by = order_by + ' ' + request.args.get('order', '')
            
        query_result = User.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 20, type=int))
        return BaseResponse(data={'users': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()
    def post(self):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()

        data = json.loads(request.data)
        result = User().from_dict(dict(data))

        return BaseResponse(data=result.to_dict()).dict()
    
userApi.add_resource(Users, '/<int:user_id>')
userApi.add_resource(UsersList, '/')
