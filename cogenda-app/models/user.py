#-*- coding:utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
import hmac

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(200))
    password = Column(String(200), default='')
    company = Column(String(200))
    email = Column(String(200))
    mobile = Column(String(20))
    role = Column(String(1))
    resource = Column(String(4000))
    notes = Column(String(4000))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now())

    def __init__(self, username, password, company, email, mobile, role, resource, notes, active=True):
        Base.__init__(self)
        self.username = username
        self.password = hmac.new('cogenda_salt', password).hexdigest()
        self.company = company
        self.email = email
        self.mobile = mobile
        self.role = role
        self.resource = resource
        self.notes = notes
        self.active = active

    def __str__(self):
        return self.username

    @staticmethod
    def is_active(self):
        return self.active

    @staticmethod
    def get_by_username(session, username):
        return session.query(User).filter(User.username==username).first()

    @staticmethod
    def get_by_uid(session, uid):
        return session.query(User).filter(User.id==uid).first()

    @staticmethod
    def update_by_uid(session, uid, _user):
        user = session.query(User).filter(User.id==uid).first()
        user.username = _user.username
        #user.password = _user.hmac.new('cogenda_salt', _user.password).hexdigest()
        user.company = _user.company
        user.email = _user.email
        user.mobile = _user.mobile
        user.role = _user.role
        user.resource = _user.resource
        user.notes = _user.notes
        user.active = _user.active
        session.commit()
        return user

    @staticmethod
    def list(session):
        return session.query(User).all()

    @staticmethod
    def delete_by_uid(session, uid):
        session.query(User).filter(User.id==uid).delete()
        session.commit()
