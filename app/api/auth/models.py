from app import db
from datetime import datetime
# import enum
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
    
ADMINUSER_LEVEL_ENUM = ['superuser', 'admin']
class AdminUser(db.Model, BaseModel):
    __tablename__ = 'admin_user'
    admin_id = Column(Integer, nullable=True, primary_key=True, unique=True)
    username = Column(String(20), nullable=False)
    password = Column(String(128), nullable=False)
    level = Column(Enum(*ADMINUSER_LEVEL_ENUM), nullable=False, default=ADMINUSER_LEVEL_ENUM[1])
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'username': self.username,
            'level': self.level,
            'create_time': self.create_time
            }
