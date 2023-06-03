from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config, Config
from flask_cors import CORS
from flask_restful import Api

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    
    jwt = JWTManager(app)
    
    from .api.v2 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    CORS(app, origins='*', supports_credentials=True)
    
    return app
