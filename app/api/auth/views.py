from flask import request
from . import auth
from .models import AdminUser
from app.models import BaseResponse

from app.utils import jwt_functions
from flask_jwt_extended import create_access_token


@auth.route('/', methods=['POST'])
def admin_login():
    if not request.is_json:
        return BaseResponse(code=400, message='Missing JSON in request').dict()
    
    if not request.json.get('username'):
        return BaseResponse(code=400, message='Missing username parameter').dict()
    if not request.json.get('password'):
        return BaseResponse(code=400, message='Missing password parameter').dict()
    
    user_info = AdminUser.query.filter_by(username=request.json.get('username')).first()
    
    if not user_info:
        return BaseResponse(code=404, message='user not found').dict()
    
    if not user_info.verify_password(request.json.get('password')):
        return BaseResponse(code=400, message='password error').dict()
    
    token = create_access_token(identity=user_info.username)
    
    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()

