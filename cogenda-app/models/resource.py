#-*- coding:utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class Resource(Base):

    __tablename__ = 'Resources'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(400))
    type = Column(String(2))
    vendor = Column(String(20))
    url = Column(String(1000))
    status = Column(String(10))
    uploaded_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __init__(self, name, type, vendor, url, status, uploaded_date=datetime.now, active=True):
        Base.__init__(self)
        self.name = name
        self.type = type
        self.vendor = vendor
        self.url = url
        self.status = status
        self.uploaded_date = uploaded_date
        self.active = active
    
    @staticmethod
    def list(session):
        return session.query(Resource).all()
