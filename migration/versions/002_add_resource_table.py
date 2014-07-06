from sqlalchemy import *
from migrate import *
from datetime import datetime

meta = MetaData()

resources = Table(
        'resources', meta,
        Column('id', Integer, nullable=False, primary_key=True),
        Column('name', String(400), nullable=False,),
        Column('type', String(1), nullable=False),
        Column('vendor', String(20), nullable=False),
        Column('url', String(1000), nullable=False),
        Column('uploaded_date', DateTime, default=datetime.now),
        Column('active', Boolean, default=True),
        )

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    resources.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    resources.drop()
