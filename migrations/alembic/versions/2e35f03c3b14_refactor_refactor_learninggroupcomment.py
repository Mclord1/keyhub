"""refactor : refactor LearningGroupComment

Revision ID: 2e35f03c3b14
Revises: 5dd2dab8c601
Create Date: 2024-04-17 23:43:51.249559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e35f03c3b14'
down_revision = '5dd2dab8c601'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('learning_group_comment', sa.Column('file_name', sa.String(length=255), nullable=True))
    op.add_column('learning_group_comment', sa.Column('file_path', sa.Text(), nullable=True))
    op.add_column('learning_group_comment', sa.Column('file_url', sa.Text(), nullable=True))
    op.add_column('learning_group_comment', sa.Column('content_type', sa.Text(), nullable=True))
    op.alter_column('learning_group_comment', 'comment',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('learning_group_comment', 'comment',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('learning_group_comment', 'content_type')
    op.drop_column('learning_group_comment', 'file_url')
    op.drop_column('learning_group_comment', 'file_path')
    op.drop_column('learning_group_comment', 'file_name')
    # ### end Alembic commands ###