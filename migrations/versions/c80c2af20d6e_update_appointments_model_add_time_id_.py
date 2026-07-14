"""Update appointments model - Add time_id column and change date data type

Revision ID: c80c2af20d6e
Revises: cd2fc1baa047
Create Date: 2026-07-14 12:43:02.278335

"""
from alembic import op
import sqlalchemy as sa


revision = 'c80c2af20d6e'
down_revision = 'cd2fc1baa047'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'time', ['time_id'], ['id'])

    op.alter_column('books', 'date',
           existing_type=sa.INTEGER(),
           type_=sa.Date(),
           postgresql_using='date::date',
           nullable=False)

def downgrade():
    op.alter_column('books', 'date',
           existing_type=sa.Date(),
           type_=sa.INTEGER(),
           nullable=True)

    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('time_id')
