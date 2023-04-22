import random
from datetime import datetime

import forgery_py

from app import db
from app.chat.models import Message, Room, Goods


class FakeGenerator:
    def __init__(self):
        # in case the tables haven't been created already
        db.drop_all()
        db.create_all()

    def generate_fake_date(self):
        return datetime.combine(forgery_py.date.date(True), datetime.utcnow().time())

    def generate_room_and_messages(self, count):
        # generate random user_id, room_id store them into an array
        user = []
        room = []
        goods = []
        for _ in range(count):
            user.append(random.randint(1, 100))
            room.append(random.randint(1, 100))
            goods.append(random.randint(1, 100))
            
        for _ in range(count):
            sample = random.sample(user, 2)
            Room(room_id=room[_],
                 goods_id=random.choice(goods),
                 seller_id=sample[0],
                 buyer_id=sample[1]).save()
            
            for __ in range(20):
                Message(room_id=room[_],
                        sender_id=random.choice(sample),
                        send_time=self.generate_fake_date(),
                        detail=forgery_py.forgery.lorem_ipsum.sentence()).save()
        
        for _ in range(count):
            Goods(uid=goods[_], seller_id=random.choice(user)).save()

    def generate_fake_data(self, count):
        # generation must follow this order, as each builds on the previous
        self.generate_room_and_messages(count)

    def start(self, count=10):
        self.generate_fake_data(count)
