from flask import request
from . import admins
from ..auth.models import AdminUser
from sqlalchemy import and_
from sqlalchemy.sql import text

from ..models import BaseResponse
from flask_jwt_extended import jwt_required
import json

from app.decorators import role_required
from .schemas import CreateAdminForm, UpdateAdminForm

from flask_restful import Resource, Api

adminApi = Api(admins)

class Admins(Resource):
    method_decorators = [role_required(['superuser'])]
    def get(self, admin_id):
        admin_info = AdminUser.query.filter_by(admin_id=admin_id).first()

        if not admin_info:
            return BaseResponse(code=404, message='admin not found').dict()

        return BaseResponse(data=admin_info.to_dict()).dict()

    def put(self, admin_id):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()
        
        if not AdminUser.query.filter_by(admin_id=admin_id).first():
            return BaseResponse(code=404, message='admin not found').dict()
        
        if not request.data:
            return BaseResponse(code=400, message='request data is empty').dict()
        
        # try:
        #     formData = CreateAdminForm(**json.loads(request.data))
        # except Exception as e:
        #     return BaseResponse(code=400, message='form format error').dict()
        
        # try:
        #     from ..auth.models import hash_and_salt_password
        #     hashed_password = hash_and_salt_password(formData.password)
        #     formData.password = hashed_password
        # except:
        #     return BaseResponse(code=400, message='password error').dict()
        
        # AdminUser.query.filter_by(admin_id=admin_id).update(formData.dict())
        
        # return BaseResponse(data=AdminUser.query.filter_by(admin_id=admin_id).first().to_dict()).dict()
        data = json.loads(request.data)
        updateData = UpdateAdminForm(**data)
        print(updateData)
        
        userObject = AdminUser.query.filter_by(admin_id=admin_id).first()
        
        if data.get('password'):
            userObject.password = data['password']

        AdminUser.query.filter_by(admin_id=admin_id).update(dict(updateData))

        return BaseResponse(data=AdminUser.query.filter_by(admin_id=admin_id).first().to_dict()).dict()

class AdminsList(Resource):
    method_decorators = [role_required(['superuser'])]
    def get(self):
        filter_condition = set()
        filter_condition.add(AdminUser.username.like('%' + request.args.get('username', '', type=str) + '%'))
        if request.args.get('admin_id', None, type=str):
            filter_condition.add(AdminUser.admin_id == request.args.get('admin_id'))
        if request.args.get('level', None, type=str):
            filter_condition.add(AdminUser.level == request.args.get('level'))
        
        # admin_list = AdminUser.query.all()
        
        # return BaseResponse(data={'admins': [i.to_dict() for i in admin_list]}).dict()
        order_by = request.args.get('order_by', '', type=str)
        order_list = ['asc', 'desc']
        if request.args.get('order') in order_list:
            order_by = order_by + ' ' + request.args.get('order', '')
            
        query_result = AdminUser.query.order_by(text(order_by)).filter(and_(*filter_condition)).paginate(page=request.args.get('page', 1, type=int), per_page=request.args.get('limit', 20, type=int))
        return BaseResponse(data={'admins': [i.to_dict() for i in query_result], 'count': query_result.total, 'page': query_result.pages}).dict()
    
    def post(self):
        if 'application/json' not in request.content_type:
            return BaseResponse(code=400, message='content type must be application/json').dict()
        
        if not request.data:
            return BaseResponse(code=400, message='request data is empty').dict()
        
        try:
            formData = CreateAdminForm(**json.loads(request.data))
        except Exception as e:
            return BaseResponse(code=400, message='form format error').dict()
        
        result = AdminUser(**formData.dict()).save()
        
        if not result.admin_id:
            return BaseResponse(code=400, message='username already exists').dict()
        
        return BaseResponse(data=result.to_dict()).dict()

adminApi.add_resource(Admins, '/<int:admin_id>')
adminApi.add_resource(AdminsList, '/')
