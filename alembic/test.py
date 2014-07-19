__author__ = 'jasonyao'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
import hmac

Base = declarative_base()


class Test(Base):
    address = Column('id',String(50),nullable=False)
