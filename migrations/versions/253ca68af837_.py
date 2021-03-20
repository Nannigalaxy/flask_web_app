"""empty message

Revision ID: 253ca68af837
Revises: d488178a75a3
Create Date: 2019-11-08 19:52:07.128281

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '253ca68af837'
down_revision = 'd488178a75a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('section', sa.String(length=2), nullable=True))
    op.drop_constraint('course_ibfk_1', 'course', type_='foreignkey')
    op.drop_column('course', 'Faculty_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('Faculty_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('course_ibfk_1', 'course', 'faculty', ['Faculty_id'], ['id'])
    op.drop_column('classes', 'section')
    # ### end Alembic commands ###