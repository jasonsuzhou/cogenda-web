#-*- coding:utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(200))
    password = Column(String(200), default='')
    email = Column(String(200))
    active = Column(Boolean, default=True)

    def __init__(self, username, password, email, active=True):
        Base.__init__(self)
        self.username = username
        self.password = password
        self.email = email
        self.active = active

    @staticmethod
    def is_active(self):
        return self.active

    @staticmethod
    def get_by_uid(session, uid):
        return session.query(User).filter(User.user_id==uid).first()
    
    @staticmethod
    def list(session):
        return session.query(User).all()
