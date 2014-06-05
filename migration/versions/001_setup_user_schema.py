from sqlalchemy import *
from migrate import *

meta = MetaData()

users = Table(
        'users', meta,
        Column('id', Integer, nullable=False, primary_key=True),
        Column('username', String(200), nullable=False,),
        Column('password', String(200), nullable=False),
        Column('email', String(200), nullable=False),
        Column('active', Boolean, default=True),
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
