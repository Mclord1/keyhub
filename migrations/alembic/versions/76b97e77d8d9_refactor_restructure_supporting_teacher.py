"""refactor : restructure supporting_teacher

Revision ID: 76b97e77d8d9
Revises: 176dbff519d3
Create Date: 2023-11-05 21:46:17.460991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76b97e77d8d9'
down_revision = '176dbff519d3'
branch_labels = None
depends_on = None



def upgrade():
    # Alter the column data type from JSON to String(350)
    op.alter_column('project', 'supporting_teachers', type_=sa.String(350))

def downgrade():
    # Revert the column data type to JSON
    op.alter_column('project', 'supporting_teachers', type_=sa.JSON())