import random
from datetime import datetime
from hashlib import md5

import forgery_py
import logging
from app import db
from app.api.v2.auth.models import AdminUser
from app.api.v2.users.models import User
from app.api.v2.goods.models import Good
from app.api.v2.wallets.models import Wallet
from app.api.v2.issues.models import Issue
from app.api.v2.orders.models import Order

import sqlalchemy
import os
from sqlalchemy.orm import Session

class FakeGenerator:
    def __init__(self):
        # engine = sqlalchemy.create_engine(os.environ.get("DATABASE_BASE_URI"))
        # with Session(engine) as session:
        #     statement = sqlalchemy.text('create database app_dev')
        #     result = session.execute(statement)

                
        db.drop_all()
        db.create_all()

    def generate_fake_date(self):
        return datetime.combine(forgery_py.date.date(True, max_delta=60), datetime.utcnow().time())
    
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
                'blocked': random.choice([True, False]),
                    })
            
            Good().from_dict({
                'seller_id': random.randint(1, count),
                'state': random.choice(Good.GOOD_STATES_ENUM),
                'game': forgery_py.forgery.address.city(),
                'title': forgery_py.forgery.lorem_ipsum.title(),
                'detail': forgery_py.forgery.lorem_ipsum.sentences(),
                'price': random.randint(1, 100) + random.random(),
                'publish_time': self.generate_fake_date(),
            })
            
            Wallet().from_dict({
                'user_id': random.randint(1, count),
                'balance': random.randint(1, 1000) + random.random(),
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
            
            Order().from_dict({
                'order_id': random.randint(1, count),
                'from_id': random.randint(1, count),
                'to_id': random.randint(1, count),
                'good_id': random.randint(1, count),
                'price': random.randint(1, 100) + random.random(),
                'state': random.choice(Order.ORDER_STATE_ENUM),
                'create_time': self.generate_fake_date(),
                'pay_time': self.generate_fake_date(),
            })
            
        logging.info('Generated {} fake goods'.format(count))
        logging.info('Generated {} fake users'.format(count))
        logging.info('Generated {} fake issues'.format(count))
        logging.info('Generated {} fake orders'.format(count))

    def start(self, count=10):
        AdminUser().from_dict({
            'username': 'superuser',
            'password': 'root',
            'level': AdminUser.ADMINUSER_LEVEL_ENUM[0],
        })
        
        self.generate_fake_app_data(count)
        self.generate_fake_admin_data(count)
