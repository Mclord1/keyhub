"""update teacher table

Revision ID: e2c130c1a259
Revises: ffaf29b23843
Create Date: 2024-02-05 21:17:49.001560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c130c1a259'
down_revision = 'ffaf29b23843'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teacher', sa.Column('years_of_experience', sa.String(length=350), nullable=True))
    op.add_column('teacher', sa.Column('has_bachelors_degree', sa.String(length=350), nullable=True))
    op.add_column('teacher', sa.Column('early_years_education', sa.String(length=350), nullable=True))
    op.add_column('teacher', sa.Column('linkedin', sa.String(length=350), nullable=True))
    op.add_column('teacher', sa.Column('how_you_heard_about_us', sa.Text(), nullable=True))
    op.add_column('teacher', sa.Column('purpose_using_the_app', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teacher', 'purpose_using_the_app')
    op.drop_column('teacher', 'how_you_heard_about_us')
    op.drop_column('teacher', 'linkedin')
    op.drop_column('teacher', 'early_years_education')
    op.drop_column('teacher', 'has_bachelors_degree')
    op.drop_column('teacher', 'years_of_experience')
    # ### end Alembic commands ###