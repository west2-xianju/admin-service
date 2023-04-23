import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask import Flask
from app import create_app, db
import click
app = create_app('development')

# @app.cli.command()
# def test():
#     """Runs the unit tests."""
#     import sys
#     import unittest

#     tests = unittest.TestLoader().discover("tests")
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.errors or result.failures:
#         sys.exit(1)

@app.cli.command()
def clean_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


@app.cli.command()
def fill_db():
    from utils.db_generator import FakeGenerator
    FakeGenerator().start()


if __name__ == '__main__':
    
    # from app.api.auth.models import AdminUser
    # from app.api.users.models import User
    # from utils.db_generator import FakeGenerator
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #     FakeGenerator().start()
    
    Flask.run(app ,debug=True)