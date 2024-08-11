"""feat : add teacher_position to TeacherProject model

Revision ID: 344b5afc251f
Revises: c37bf702becd
Create Date: 2023-11-05 18:42:26.361762

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '344b5afc251f'
down_revision = 'c37bf702becd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('teacher_project', sa.Column('teacher_position', sa.String(350), nullable=True))


def downgrade():
    op.drop_column('teacher_project', 'teacher_position')
