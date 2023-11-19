"""feat : add academic & terms table

Revision ID: d779fb30c49b
Revises: 1c03c51ecbab
Create Date: 2023-11-18 15:54:58.895245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd779fb30c49b'
down_revision = '1c03c51ecbab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('academic_year',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['school.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('term',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['school.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('term')
    op.drop_table('academic_year')
    # ### end Alembic commands ###