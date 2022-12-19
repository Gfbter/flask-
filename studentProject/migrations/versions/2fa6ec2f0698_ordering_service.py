"""ordering service

Revision ID: 2fa6ec2f0698
Revises: ab59c9f8a40e
Create Date: 2022-10-06 20:17:37.185041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fa6ec2f0698'
down_revision = 'ab59c9f8a40e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'order', 'area', ['area_id'], ['id'])
    op.create_foreign_key(None, 'order', 'employee', ['employee_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_constraint(None, 'order', type_='foreignkey')
    # ### end Alembic commands ###
