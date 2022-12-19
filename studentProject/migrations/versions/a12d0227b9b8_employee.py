"""employee

Revision ID: a12d0227b9b8
Revises: ea1adfecabab
Create Date: 2022-09-27 02:20:35.934114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a12d0227b9b8'
down_revision = 'ea1adfecabab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_area_name'), 'area', ['name'], unique=True)
    op.create_table('employee',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('profession', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employee_name'), 'employee', ['name'], unique=False)
    op.create_index(op.f('ix_employee_profession'), 'employee', ['profession'], unique=False)
    op.create_table('service',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('price', sa.String(length=12), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_name'), 'service', ['name'], unique=True)
    op.create_index(op.f('ix_service_price'), 'service', ['price'], unique=False)
    op.add_column('order', sa.Column('employee_id', sa.Integer(), nullable=True))
    op.add_column('order', sa.Column('area_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'employee', ['employee_id'], ['id'])
    op.create_foreign_key(None, 'order', 'area', ['area_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'area_id')
    op.drop_column('order', 'employee_id')
    op.drop_index(op.f('ix_service_price'), table_name='service')
    op.drop_index(op.f('ix_service_name'), table_name='service')
    op.drop_table('service')
    op.drop_index(op.f('ix_employee_profession'), table_name='employee')
    op.drop_index(op.f('ix_employee_name'), table_name='employee')
    op.drop_table('employee')
    op.drop_index(op.f('ix_area_name'), table_name='area')
    op.drop_table('area')
    # ### end Alembic commands ###
