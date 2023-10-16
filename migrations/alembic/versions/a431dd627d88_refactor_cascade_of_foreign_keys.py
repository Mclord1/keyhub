"""refactor cascade of foreign keys

Revision ID: a431dd627d88
Revises: d627bf96e83f
Create Date: 2023-10-14 08:29:31.129303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a431dd627d88'
down_revision = 'd627bf96e83f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'project', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='unique')
    # ### end Alembic commands ###