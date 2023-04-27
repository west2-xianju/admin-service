from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config, Config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    
    jwt = JWTManager(app)

    # from .api.v1.chat import chat as chat_blueprint
    # app.register_blueprint(chat_blueprint)
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # from .api.dev import dev as dev_blueprint
    # app.register_blueprint(dev_blueprint, url_prefix='/dev')
    
    # from .api.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # from .api.users import users as users_blueprint
    # app.register_blueprint(users_blueprint, url_prefix='/users')
    
    return app
