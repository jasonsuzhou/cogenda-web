from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    add_column = DDL('ALTER TABLE resources ADD COLUMN description VARCHAR(400)')
    migrate_engine.execute(add_column)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    remove_column = DDL('ALTER TABLE resources DROP COLUMN description')
    migrate_engine.execute(remove_column)
