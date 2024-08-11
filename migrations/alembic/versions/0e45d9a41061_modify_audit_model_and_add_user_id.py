"""modify audit model and add user id

Revision ID: 0e45d9a41061
Revises: 1ab73d1fb384
Create Date: 2023-10-29 16:14:13.072009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e45d9a41061'
down_revision = '1ab73d1fb384'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('audit', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('audit_admin_id_fkey', 'audit', type_='foreignkey')
    op.create_foreign_key(None, 'audit', 'user', ['user_id'], ['id'])
    op.drop_column('audit', 'admin_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('audit', sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'audit', type_='foreignkey')
    op.create_foreign_key('audit_admin_id_fkey', 'audit', 'admin', ['admin_id'], ['id'])
    op.drop_column('audit', 'user_id')
    # ### end Alembic commands ###
