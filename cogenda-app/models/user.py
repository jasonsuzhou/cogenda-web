#-*- coding:utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

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
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now)

    def __init__(self, username, password, company, email, mobile, role, resource, notes, active=True, created_date=datetime.now, updated_date=datetime.now):
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
        self.created_date = created_date
        self.updated_date = updated_date

    @staticmethod
    def is_active(self):
        return self.active

    @staticmethod
    def get_by_uid(session, uid):
        return session.query(User).filter(User.id==uid).first()

    @staticmethod
    def update_by_uid(session, uid, company):
        user = session.query(User).filter(User.id==uid).first()
        user.company = company
        session.commit()
        return user

    @staticmethod
    def list(session):
        return session.query(User).all()

    @staticmethod
    def delete_by_uid(session, uid):
        session.query(User).filter(User.id==uid).delete()
        session.commit()
