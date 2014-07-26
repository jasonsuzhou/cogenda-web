"""empty message

Revision ID: 113b11ec956f
Revises: 14d99172d52e
Create Date: 2014-07-20 13:46:47.262183

"""

# revision identifiers, used by Alembic.
revision = '113b11ec956f'
down_revision = '14d99172d52e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index("file_unique_per_vendor", "resources", ["name", "vendor"], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("file_unique_per_vendor")
    ### end Alembic commands ###
