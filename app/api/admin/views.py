from flask import request
from . import admin
from ..auth.models import AdminUser
from sqlalchemy import and_
from sqlalchemy.sql import text

from ...models import BaseResponse
from flask_jwt_extended import jwt_required
import json

@admin.route('/', methods=['GET'])
@jwt_required()
def get_admin_list():
    
    admin_list = AdminUser.query.all()
    
    return BaseResponse(data={'admins': [i.to_dict() for i in admin_list]}).dict()


@admin.route('/<int:admin_id>', methods=['GET'])
@jwt_required()
def get_admin_info(admin_id):
    if not AdminUser.query.filter_by(admin_id=admin_id).first():
        return BaseResponse(code=404, message='admin not found').dict()
    
    admin_info = AdminUser.query.filter_by(admin_id=admin_id).first()
    
    return BaseResponse(data=admin_info.to_dict()).dict()


@admin.route('/', methods=['POST'])
@jwt_required()
def create_admin():
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    if data['level'] not in AdminUser.ADMINUSER_LEVEL_ENUM:
        return BaseResponse(code=400, message='level must be in {}'.format(AdminUser.ADMINUSER_LEVEL_ENUM)).dict()
    
    result = AdminUser().from_dict(data)
    
    return BaseResponse(data=result.to_dict()).dict()

@admin.route("/<int:admin_id>", methods=["PUT"])
@jwt_required()
def modify_admin(admin_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not AdminUser.query.filter_by(admin_id=admin_id).first():
        return BaseResponse(code=404, message='admin not found').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    
    from ..auth.models import hash_and_salt_password
    hashed_password = hash_and_salt_password(data['password'])
    data.update({'password': hashed_password})
    
    AdminUser.query.filter_by(admin_id=admin_id).update(data)
    
    return BaseResponse(data=AdminUser.query.filter_by(admin_id=admin_id).first().to_dict()).dict()

