"""add relationship between role and admin

Revision ID: 9bd4fef52476
Revises: a1368f6f75d0
Create Date: 2023-08-31 08:54:07.406642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bd4fef52476'
down_revision = 'a1368f6f75d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'role', 'admin', ['admin_id'], ['id'])
    op.drop_column('role', 'created_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('created_by', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'role', type_='foreignkey')
    op.drop_column('role', 'admin_id')
    # ### end Alembic commands ###