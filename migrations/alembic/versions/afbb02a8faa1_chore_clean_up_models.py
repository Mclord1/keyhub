"""chore : clean up models

Revision ID: afbb02a8faa1
Revises: cd4f4f106528
Create Date: 2023-11-19 01:34:02.616283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afbb02a8faa1'
down_revision = 'cd4f4f106528'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('learning_group_file', sa.Column('file_url', sa.Text(), nullable=False))
    op.add_column('project_file', sa.Column('file_url', sa.Text(), nullable=False))
    op.add_column('student', sa.Column('profile_image', sa.Text(), nullable=True))
    op.add_column('student_file', sa.Column('file_url', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student_file', 'file_url')
    op.drop_column('student', 'profile_image')
    op.drop_column('project_file', 'file_url')
    op.drop_column('learning_group_file', 'file_url')
    # ### end Alembic commands ###
