from flask import request
from . import auth
from app.models import BaseResponse

from app.utils import jwt_functions
from flask_jwt_extended import create_access_token


@auth.route('/', methods=['POST'])
def admin_login():
    
    token = create_access_token(123)

    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()

