"""chore : update admin table

Revision ID: c271f97b0508
Revises: b980aa84e48b
Create Date: 2023-11-25 23:42:19.197470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c271f97b0508'
down_revision = 'b980aa84e48b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('profile_image', sa.Text(), nullable=True))
    op.drop_constraint('checklist_question_created_by_fkey', 'checklist_question', type_='foreignkey')
    op.create_foreign_key(None, 'checklist_question', 'admin', ['created_by'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'checklist_question', type_='foreignkey')
    op.create_foreign_key('checklist_question_created_by_fkey', 'checklist_question', 'user', ['created_by'], ['id'], ondelete='SET NULL')
    op.drop_column('admin', 'profile_image')
    # ### end Alembic commands ###