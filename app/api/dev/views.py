from flask import request
from . import dev

from ...models import BaseResponse
from flask_jwt_extended import create_access_token

@dev.route('/auth/<int:user_id>', methods=['GET'])
def get_admin_token(user_id):
    jwt_token = create_access_token(user_id)
    return BaseResponse(data={'token': jwt_token}).dict()