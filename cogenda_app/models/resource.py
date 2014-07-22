# -*- coding:utf-8 -*-


from _base import Base
from sqlalchemy import and_
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import aliased
from datetime import datetime
from lib import const


class Resource(Base):

    __tablename__ = 'Resources'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(400))
    description = Column(String(400))
    type = Column(String(2))
    vendor = Column(String(20))
    url = Column(String(1000))
    uploaded_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __init__(self, name, description, type, vendor, url, uploaded_date=datetime.now(), active=True):
        Base.__init__(self)
        self.name = name
        self.description = description
        self.type = type
        self.vendor = vendor
        self.url = url
        self.uploaded_date = uploaded_date
        self.active = active

    @property
    def jsonify(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'vendor': self.vendor,
            'url': self.url,
            'uploaded_date': datetime.strftime(self.uploaded_date, '%Y-%m-%d %H:%M:%S'),
            'active': self.active
        }

    @staticmethod
    def fetch_grouped_resources(session):
        """
        API for grouped resources by resource name, result will be an tuple contained array. like following:
        (<models.resource.Resource object at 0x11134e050>, None) // only one vendor -> e.g. aws
        (<models.resource.Resource object at 0x11134e110>, <models.resource.Resource object at 0x11134e190>) //exists both oss & aws
        (<models.resource.Resource object at 0x11134e210>, <models.resource.Resource object at 0x11134e290>) //exists both oss & aws
        (<models.resource.Resource object at 0x11134e310>, None) // only one vendor -> e.g. oss
        """
        ParentResource = aliased(Resource, name='parent_resource')
        records = session.query(Resource, ParentResource).outerjoin(
            ParentResource,
            and_(
                Resource.name == ParentResource.name,
                Resource.vendor != ParentResource.vendor
            )
        ).group_by(Resource.name).all()
        return records

    @staticmethod
    def fetch_grouped_active_resources(session):
        """
        API for grouped active resources by resource name, result will be an tuple contained array. like following:
        (<models.resource.Resource object at 0x11134e050>, None) // only one vendor -> e.g. aws
        (<models.resource.Resource object at 0x11134e110>, <models.resource.Resource object at 0x11134e190>) //exists both oss & aws
        (<models.resource.Resource object at 0x11134e210>, <models.resource.Resource object at 0x11134e290>) //exists both oss & aws
        (<models.resource.Resource object at 0x11134e310>, None) // only one vendor -> e.g. oss
        """
        ParentResource = aliased(Resource, name='parent_resource')
        records = session.query(Resource, ParentResource).outerjoin(
            ParentResource,
            and_(
                Resource.name == ParentResource.name,
                Resource.vendor != ParentResource.vendor,
                Resource.active == ParentResource.active)
        ).filter(Resource.active == True).group_by(Resource.name).all()
        return records

    @staticmethod
    def fetch_grouped_private_resources(session):
        """
        API for grouped resources by resource name, result will be an tuple contained array. like following:
        (<models.resource.Resource object at 0x11134e050>, None) // only one vendor -> e.g. aws
        (<models.resource.Resource object at 0x11134e110>, <models.resource.Resource object at 0x11134e190>) //exists both oss & aws
        (<models.resource.Resource object at 0x11134e210>, <models.resource.Resource object at 0x11134e290>) //exists both oss & aws
        (<models.resource.Resource object at 0x11134e310>, None) // only one vendor -> e.g. oss
        """
        ParentResource = aliased(Resource, name='parent_resource')
        records = session.query(Resource, ParentResource).outerjoin(
            ParentResource,
            and_(
                Resource.name == ParentResource.name,
                Resource.vendor != ParentResource.vendor
            )
        ).filter(Resource.type == const.RESOURCE_TYPE_PRIVATE).group_by(Resource.name).all()
        return records

    @staticmethod
    def list(session):
        return session.query(Resource).order_by(Resource.name.desc(), Resource.id.desc()).all()

    @staticmethod
    def list_active_resources(session):
        return session.query(Resource).filter(Resource.active == True).order_by(Resource.name.desc(), Resource.id.desc()).all()

    @staticmethod
    def list_resource_by_vendor(session, vendor):
        return session.query(Resource).filter(Resource.vendor == vendor).all()

    @staticmethod
    def list_resource_by_type(session, type):
        return session.query(Resource).filter(Resource.type == type, Resource.active == True).all()

    @staticmethod
    def get_by_rid(session, rid):
        return session.query(Resource).filter(Resource.id == rid).first()

    @staticmethod
    def get_by_rids(session, rids):
        return session.query(Resource).filter(Resource.id.in_(rids)).all()

    @staticmethod
    def get_resource_by_name_vendor(session, name, vendor):
        return session.query(Resource).filter(Resource.name == name, Resource.vendor == vendor).first()

    @staticmethod
    def update_resource(session, resource, json_resource):
        resource.description = json_resource['desc']
        resource.type = json_resource['type']
        resource.active = json_resource['active']
        session.commit()
        return resource

    @staticmethod
    def delete_resource_by_name_vendor(session, name, vendor):
        session.query(Resource).filter(Resource.name == name, Resource.vendor == vendor).delete()
        session.commit()
