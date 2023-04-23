from flask import Blueprint

goods = Blueprint("users", __name__)

from . import views, models
