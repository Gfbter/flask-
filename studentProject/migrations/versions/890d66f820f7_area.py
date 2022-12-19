"""area

Revision ID: 890d66f820f7
Revises: 07e69ed6ef69
Create Date: 2022-09-27 01:43:52.893529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '890d66f820f7'
down_revision = '07e69ed6ef69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_area_name'), 'area', ['name'], unique=True)
    op.create_index(op.f('ix_area_status'), 'area', ['status'], unique=False)
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
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('expiration_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_date'), 'order', ['date'], unique=False)
    op.create_index(op.f('ix_order_expiration_date'), 'order', ['expiration_date'], unique=False)
    op.add_column('car', sa.Column('car_number', sa.String(length=9), nullable=True))
    op.create_index(op.f('ix_car_car_number'), 'car', ['car_number'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_car_car_number'), table_name='car')
    op.drop_column('car', 'car_number')
    op.drop_index(op.f('ix_order_expiration_date'), table_name='order')
    op.drop_index(op.f('ix_order_date'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_service_price'), table_name='service')
    op.drop_index(op.f('ix_service_name'), table_name='service')
    op.drop_table('service')
    op.drop_index(op.f('ix_employee_profession'), table_name='employee')
    op.drop_index(op.f('ix_employee_name'), table_name='employee')
    op.drop_table('employee')
    op.drop_index(op.f('ix_area_status'), table_name='area')
    op.drop_index(op.f('ix_area_name'), table_name='area')
    op.drop_table('area')
    # ### end Alembic commands ###
