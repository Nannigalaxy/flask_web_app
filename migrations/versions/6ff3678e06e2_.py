"""empty message

Revision ID: 6ff3678e06e2
Revises: 9710882185b1
Create Date: 2019-11-15 14:52:39.513279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ff3678e06e2'
down_revision = '9710882185b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ia_1_ibfk_1', 'ia_1', type_='foreignkey')
    op.create_foreign_key(None, 'ia_1', 'student', ['usn'], ['usn'], onupdate='cascade', ondelete='cascade')
    op.drop_constraint('ia_2_ibfk_1', 'ia_2', type_='foreignkey')
    op.create_foreign_key(None, 'ia_2', 'student', ['usn'], ['usn'], onupdate='cascade', ondelete='cascade')
    op.drop_constraint('ia_3_ibfk_1', 'ia_3', type_='foreignkey')
    op.create_foreign_key(None, 'ia_3', 'student', ['usn'], ['usn'], onupdate='cascade', ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ia_3', type_='foreignkey')
    op.create_foreign_key('ia_3_ibfk_1', 'ia_3', 'student', ['usn'], ['usn'], onupdate='CASCADE')
    op.drop_constraint(None, 'ia_2', type_='foreignkey')
    op.create_foreign_key('ia_2_ibfk_1', 'ia_2', 'student', ['usn'], ['usn'], onupdate='CASCADE')
    op.drop_constraint(None, 'ia_1', type_='foreignkey')
    op.create_foreign_key('ia_1_ibfk_1', 'ia_1', 'student', ['usn'], ['usn'], onupdate='CASCADE')
    # ### end Alembic commands ###
