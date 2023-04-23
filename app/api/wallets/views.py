from flask import request
from . import wallets
from .models import Wallet
from sqlalchemy import and_
from sqlalchemy.sql import text

from ...models import BaseResponse
from flask_jwt_extended import jwt_required
import json


@wallets.route('/<int:wallet_id>', methods=['GET'])
@jwt_required()
def get_wallet_info(wallet_id):
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()

    return BaseResponse(data=Wallet.query.filter_by(wallet_id=wallet_id).first().to_dict()).dict()

@wallets.route('/<int:wallet_id>', methods=['PUT'])
@jwt_required()
def charge_wallet(wallet_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    
    if 'amount' not in data:
        return BaseResponse(code=400, message='amount is required').dict()
    
    wallet_info = Wallet.query.filter_by(wallet_id=wallet_id).first()
    wallet_info.balance += data['amount']
    wallet_info.save()
    
    return BaseResponse(data=wallet_info.to_dict()).dict()

@wallets.route('/<int:wallet_id>', methods=['DELETE'])
@jwt_required()
def withdraw_wallet(wallet_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()
    
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    
    if 'amount' not in data:
        return BaseResponse(code=400, message='amount is required').dict()
    
    wallet_info = Wallet.query.filter_by(wallet_id=wallet_id).first()
    wallet_info.balance -= data['amount']
    wallet_info.save()
    
    return BaseResponse(data=wallet_info.to_dict()).dict()


@wallets.route('/<int:wallet_id>', methods=['PATCH'])
@jwt_required()
def block_wallet(wallet_id):
    if request.content_type != 'application/json':
        return BaseResponse(code=400, message='content type must be application/json').dict()
    if not Wallet.query.filter_by(wallet_id=wallet_id).first():
        return BaseResponse(code=404, message='wallet not found').dict()
    if not request.data:
        return BaseResponse(code=400, message='request data is empty').dict()
    
    data = json.loads(request.data)
    if 'state' not in data:
        return BaseResponse(code=400, message='state is required').dict()
    if data['state'] not in Wallet.WALLET_STATES_ENUM:
        return BaseResponse(code=400, message='state is invalid').dict()
    
    wallet_info = Wallet.query.filter_by(wallet_id=wallet_id).first()
    wallet_info.state = data['state']
    
    return BaseResponse(data=wallet_info.to_dict()).dict()