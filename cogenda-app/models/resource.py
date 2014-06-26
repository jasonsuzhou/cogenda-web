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
    #TODO: inconsistent with database type. Should alter to Boolean
    status = Column(Boolean, default=True)
    uploaded_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __init__(self, name, type, vendor, url, status, uploaded_date=datetime.now(), active=True):
        Base.__init__(self)
        self.name = name
        self.type = type
        self.vendor = vendor
        self.url = url
        self.status = status
        self.uploaded_date = uploaded_date
        self.active = active

    # def __init__(self, type, active=True):
    #     Base.__init__(self)
    #     self.type = type
    #     self.active = active
    
    @staticmethod
    def list(session):
        return session.query(Resource).all()

    @staticmethod
    def get_by_rid(session, rid):
        return session.query(Resource).filter(Resource.id==rid).first()

    @staticmethod
    def get_resource_by_name_vendor(session, name, vendor):
        return session.query(Resource).filter(Resource.name==name, Resource.vendor==vendor).first()
    

    @staticmethod
    def update_resource(session, resource, _resource):
        if resource.type != _resource.type:
            resource.type = _resource.type
        if resource.active != _resource.active:
            resource.active = _resource.active
        session.commit()
        return resource
