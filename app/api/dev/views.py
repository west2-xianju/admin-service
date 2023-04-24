from flask import request
from . import dev

from ..goods.models import Good

from ...models import BaseResponse
from flask_jwt_extended import create_access_token

@dev.route('/auth/<int:user_id>', methods=['GET'])
def get_admin_token(user_id):
    jwt_token = create_access_token(user_id)
    return BaseResponse(data={'token': jwt_token}).dict()

@dev.route('/goods', methods=['PUT'])
def pass_all_censors():
    pending_goods = Good.query.filter_by(state=Good.GOOD_STATES_ENUM[0]).all()
    for _ in pending_goods:
        _.state = Good.GOOD_STATES_ENUM[1]
        
    return BaseResponse(data={'goods': [i.to_dict() for i in pending_goods]}).dict()