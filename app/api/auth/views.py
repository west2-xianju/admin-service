from flask import request
from . import auth
from app.models import BaseResponse

from app.utils import jwt_functions


@auth.route('/<int:user_id>', methods=['GET'])
def get_user_jwt(user_id):
    token = jwt_functions.generate_jwt({'user_id': user_id})
    

    return BaseResponse(data={'token': token, 'token_type': 'Bearer'}).dict()

