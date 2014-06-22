from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    resources = Table('resources', meta, autoload=True)
    index = Index("file_unique_per_vendor", resources.c.name, resources.c.vendor,  unique=True)
    index.create(migrate_engine)



def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    resources = Table('resources', meta, autoload=True)
    index = Index("file_unique_per_vendor", resources.c.name, resources.c.vendor,  unique=True)
    index.drop(migrate_engine)
