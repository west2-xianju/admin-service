from app import db
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import synonym



class BaseModel:
    """Base for all models, providing save, delete and from_dict methods."""

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """Deletes this model from the db (through db.session)"""
        db.session.delete(self)
        self.__commit()

    def save(self):
        """Adds this model to the db (through db.session)"""
        db.session.add(self)
        self.__commit()
        return self

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()

class Good(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'good'
    
    GOOD_STATES_ENUM = ['pending', 'released', 'locked', 'sold', 'reported', 'canceled', 'deleted']
    good_id = Column('uid', Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    state = Column(Enum(*GOOD_STATES_ENUM), nullable=False, default=GOOD_STATES_ENUM[0])
    game = Column(String(256))
    title = Column(String(256))
    detail = Column(String(256))
    price = Column(DECIMAL(10, 2))
    publish_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'uid': self.good_id,
            'seller_id': self.seller_id,
            'state': self.state,
            'game': self.game,
            'title': self.title,
            'detail': self.detail,
            'price': self.price,
            'publish_time': self.publish_time
            }
        

