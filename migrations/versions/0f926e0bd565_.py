"""empty message

Revision ID: 0f926e0bd565
Revises: 3c039d3d9ad7
Create Date: 2019-11-08 17:54:33.082961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f926e0bd565'
down_revision = '3c039d3d9ad7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('faculty', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('faculty', 'is_admin')
    # ### end Alembic commands ###
