import random
from datetime import datetime
from hashlib import md5

import forgery_py
import logging
from app import db
from app.api.users.models import User


class FakeGenerator:
    def __init__(self):
        # in case the tables haven't been created already
        db.drop_all()
        db.create_all()

    def generate_fake_date(self):
        return datetime.combine(forgery_py.date.date(True), datetime.utcnow().time())
    
    def generate_fake_app_data(self, count):
        for _ in range(count):
            User().from_dict({
                'username': forgery_py.internet.user_name(True),
                'nickname': forgery_py.name.full_name(),
                'password': '123456',
                'email': forgery_py.forgery.internet.email_address(),
                'realname': forgery_py.name.full_name(),
                'id_number': forgery_py.forgery.address.phone(),
                'register_time': self.generate_fake_date(),
                    }).save()
            
        logging.info('Generated {} fake users'.format(count))

    def start(self, count=10):
        self.generate_fake_app_data(count)
