from sqlalchemy import *
from migrate import *
from datetime import datetime

meta = MetaData()

users = Table(
        'users', meta,
        Column('id', Integer, nullable=False, primary_key=True),
        Column('username', String(200), nullable=False),
        Column('password', String(20), nullable=False),
        Column('company', String(400), nullable=False),
        Column('email', String(200), nullable=False),
        Column('mobile', String(20), nullable=False),
        Column('role', String(1), nullable=False),
        Column('resource', String(1000), nullable=False),
        Column('notes', String(4000), nullable=False),
        Column('active', Boolean, default=True),
        Column('created_date', DateTime, default=datetime.now),
        Column('updated_date', DateTime, default=datetime.now),
        )

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    users.drop()
