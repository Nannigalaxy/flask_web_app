"""empty message

Revision ID: 41ab1b06c197
Revises: 0ae54c3a6984
Create Date: 2019-11-09 17:52:36.519221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ab1b06c197'
down_revision = '0ae54c3a6984'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('class_courses_ibfk_1', 'class_courses', type_='foreignkey')
    op.drop_constraint('class_courses_ibfk_3', 'class_courses', type_='foreignkey')
    op.drop_constraint('class_courses_ibfk_2', 'class_courses', type_='foreignkey')
    op.create_foreign_key(None, 'class_courses', 'classes', ['class_id'], ['id'], onupdate='cascade')
    op.create_foreign_key(None, 'class_courses', 'course', ['course_code'], ['code'], onupdate='cascade')
    op.create_foreign_key(None, 'class_courses', 'faculty', ['faculty_id'], ['id'], onupdate='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'class_courses', type_='foreignkey')
    op.drop_constraint(None, 'class_courses', type_='foreignkey')
    op.drop_constraint(None, 'class_courses', type_='foreignkey')
    op.create_foreign_key('class_courses_ibfk_2', 'class_courses', 'course', ['course_code'], ['code'])
    op.create_foreign_key('class_courses_ibfk_3', 'class_courses', 'faculty', ['faculty_id'], ['id'])
    op.create_foreign_key('class_courses_ibfk_1', 'class_courses', 'classes', ['class_id'], ['id'])
    # ### end Alembic commands ###
