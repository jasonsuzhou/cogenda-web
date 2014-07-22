# -*- coding:utf-8 -*-
from _base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
import hmac


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

    @property
    def jsonify(self):
        columns = self._sa_class_manager.mapper.mapped_table.columns
        jsonified_user = {}
        for col in columns:
            col_name = col.name
            if col_name != 'created_date' and col_name != 'updated_date':
                jsonified_user[col_name] = getattr(self, col_name)
        return jsonified_user
    

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
    def update_user(session, origin_user, json_user, salt):
        # build user model
        origin_user.username = json_user['username']
        origin_user.passoword = hmac.new(salt, json_user['password']).hexdigest()
        origin_user.company = json_user['company']
        origin_user.email = json_user['email']
        origin_user.mobile = json_user['mobile']
        origin_user.role = json_user['role']
        origin_user.resource = json_user['resource']
        origin_user.notes = json_user['notes']
        origin_user.active = json_user['active']
        origin_user.updated_date = datetime.now()
        session.commit()
        return origin_user

    @staticmethod
    def list(session):
        return session.query(User).all()

    @staticmethod
    def delete_by_uid(session, uid):
        session.query(User).filter(User.id == uid).delete()
        session.commit()

    @staticmethod
    def update_user_password(session, user, password, salt):
        user.password = hmac.new(salt, password).hexdigest()
        session.commit()
        return user
