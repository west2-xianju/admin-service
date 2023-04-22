import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDB = os.environ.get("DATABASE_BASE_URI")

def create_sqlalchemy_uri(db_name):
    return BASEDB + db_name
    # return "sqlite:///" + os.path.join(BASEDIR, db_name)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret key, just for testing"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = 'testing'
    JWT_EXPIRY = 3600

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = create_sqlalchemy_uri("chat_dev")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlalchemy_uri("chat_test")
    WTF_CSRF_ENABLED = False
    import logging

    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.DEBUG)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = create_sqlalchemy_uri("chat")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
