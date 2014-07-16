# -*- coding:utf-8 -*-


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
        self.password = password
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
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_uid(session, uid):
        return session.query(User).filter(User.id == uid).first()

    @staticmethod
    def update_user(session, user, _user):
        if user.username != _user.username:
            user.username = _user.username
        if user.company != _user.company:
            user.company = _user.company
        if user.email != _user.email:
            user.email = _user.email
        if user.mobile != _user.mobile:
            user.mobile = _user.mobile
        if user.role != _user.role:
            user.role = _user.role
        if user.resource != _user.resource:
            user.resource = _user.resource
        if user.notes != _user.notes:
            user.notes = _user.notes
        if user.active != _user.active:
            user.active = _user.active
        session.commit()
        return user

    @staticmethod
    def list(session):
        return session.query(User).all()

    @staticmethod
    def delete_by_uid(session, uid):
        session.query(User).filter(User.id == uid).delete()
        session.commit()

    @staticmethod
    def update_user_password(session, user, password):
        user.password = hmac.new('cogenda_salt', password).hexdigest()
        session.commit()
        return user
