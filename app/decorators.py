from flask import abort, request, session
from app.utils import jwt_functions
from app.models import BaseResponse
import functools

# get bearer jwt token from http authorization header.
# verify it check if valid

def login_required(f):
    def wrapper(*args, **kwargs):
        @functools.wraps(f)
        def decorator(*args, **kwargs):
            if not request.headers.get('Authorization'):
                return BaseResponse(code=401, message='No token').dict()

            token = request.headers.get('Authorization').split(' ')[1]
            payload = jwt_functions.verify_jwt(token)

            if not payload:
                return BaseResponse(code=401, message='invalid token').dict()

            return f(*args, **kwargs)
        return decorator
    
    return wrapper

def role_required(role_list):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not request.headers.get('Authorization'):
                return BaseResponse(code=401, message='No token').dict()

            token = request.headers.get('Authorization').split(' ')[1]
            payload = jwt_functions.verify_jwt(token)

            if not payload:
                return BaseResponse(code=401, message='invalid token').dict()

            if payload['role'] not in role_list:
                return BaseResponse(code=401, message='permission denied').dict()

            return f(*args, **kwargs)
        return wrapper
    return decorator

