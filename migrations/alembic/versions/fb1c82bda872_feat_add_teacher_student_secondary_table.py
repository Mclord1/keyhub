"""feat : add teacher_student secondary table

Revision ID: fb1c82bda872
Revises: 2e644a7e3177
Create Date: 2023-10-25 20:46:44.711522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb1c82bda872'
down_revision = '2e644a7e3177'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher_student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_student')
    # ### end Alembic commands ###