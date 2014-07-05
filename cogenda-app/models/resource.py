#-*- coding:utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class Resource(Base):

    __tablename__ = 'Resources'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(400))
    description = Column(String(400))
    type = Column(String(2))
    vendor = Column(String(20))
    url = Column(String(1000))
    status = Column(Boolean, default=True)
    uploaded_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __init__(self, name, description, type, vendor, url, status, uploaded_date=datetime.now(), active=True):
        Base.__init__(self)
        self.name = name
        self.description = description
        self.type = type
        self.vendor = vendor
        self.url = url
        self.status = status
        self.uploaded_date = uploaded_date
        self.active = active

    @staticmethod
    def list(session):
        return session.query(Resource).all()

    @staticmethod
    def list_resource_by_vendor(session, vendor):
        return session.query(Resource).filter(Resource.vendor==vendor).all()

    @staticmethod
    def get_by_rid(session, rid):
        return session.query(Resource).filter(Resource.id==rid).first()

    @staticmethod
    def get_resource_by_name_vendor(session, name, vendor):
        return session.query(Resource).filter(Resource.name==name, Resource.vendor==vendor).first()
    

    @staticmethod
    def update_resource(session, resource, desc, type, active):
        if resource.description != desc:
            resource.description = desc
        if resource.type != type:
            resource.type = type
        if resource.active != active:
            resource.active = active
        session.commit()
        return resource


    @staticmethod
    def delete_resource_by_name_vendor(session, name, vendor):
        session.query(Resource).filter(Resource.name==name, Resource.vendor==vendor).delete()
        session.commit()
