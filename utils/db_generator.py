import random
from datetime import datetime
from hashlib import md5

import forgery_py
import logging
from app import db
from app.api.auth.models import AdminUser
from app.api.users.models import User
from app.api.goods.models import Good
from app.api.wallets.models import Wallet
from app.api.issues.models import Issue

class FakeGenerator:
    def __init__(self):
        # in case the tables haven't been created already
        db.drop_all()
        db.create_all()

    def generate_fake_date(self):
        return datetime.combine(forgery_py.date.date(True), datetime.utcnow().time())
    
    def generate_fake_admin_data(self, count):
        for _ in range(count):
            AdminUser().from_dict({
                'username': forgery_py.internet.user_name(True),
                'password': '123456',
                'level': random.choice(AdminUser.ADMINUSER_LEVEL_ENUM),
            })
        logging.info('Generated %d fake admin users.' % count)
    
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
                    })
            
            Good().from_dict({
                'seller_id': random.randint(1, count),
                'state': random.choice(Good.GOOD_STATES_ENUM),
                'game': forgery_py.forgery.address.city(),
                'title': forgery_py.forgery.lorem_ipsum.title(),
                'detail': forgery_py.forgery.lorem_ipsum.sentences(),
                'price': random.randint(1, 100),
                'publish_time': self.generate_fake_date(),
            })
            
            Wallet().from_dict({
                'user_id': random.randint(1, count),
                'balance': random.randint(1, 1000),
                'state': random.choice(Wallet.WALLET_STATES_ENUM),
            })
            
            Issue().from_dict({
                'seller_id': random.randint(1, count),
                'buyer_id': random.randint(1, count),
                'accuser_id': random.randint(1, count),
                'reason': forgery_py.lorem_ipsum.sentence(),
                'order_id': random.randint(1, count),
                'judge_result': random.choice(Issue.JUDGE_RESULT_ENUM),
                'judge_reason': forgery_py.lorem_ipsum.sentence(),
                'judge_time': self.generate_fake_date(),
                'state': random.choice(Issue.ISSUE_STATE_ENUM),
                'judger_id': random.randint(1, count),
            })
            
        logging.info('Generated {} fake goods'.format(count))
        logging.info('Generated {} fake users'.format(count))
        logging.info('Generated {} fake issues'.format(count))

    def start(self, count=10):
        self.generate_fake_app_data(count)
        self.generate_fake_admin_data(count)
