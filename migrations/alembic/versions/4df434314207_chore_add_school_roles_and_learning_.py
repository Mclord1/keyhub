"""chore : add school roles and learning group models

Revision ID: 4df434314207
Revises: bb81c2a5c3a0
Create Date: 2023-10-23 06:38:01.225957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4df434314207'
down_revision = 'bb81c2a5c3a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('learning_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=350), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('isDeactivated', sa.Boolean(), nullable=True),
    sa.Column('deactivate_reason', sa.String(length=450), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['school.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('school_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['school.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('school_role_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.Column('school_role_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['school_role_id'], ['school_role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('school_user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('school_role_id', sa.Integer(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['school.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['school_role_id'], ['school_role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('learning_group_teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('learning_group_id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['learning_group_id'], ['learning_group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('learning_group_students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('learning_group_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['learning_group_id'], ['learning_group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('learning_group_projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('learning_group_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['learning_group_id'], ['learning_group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('school_role_id', sa.Integer(), nullable=True))
    op.drop_constraint('user_role_id_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'school_role', ['school_role_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_role_id_fkey', 'user', 'role', ['role_id'], ['id'], ondelete='CASCADE')
    op.drop_column('user', 'school_role_id')
    op.drop_table('learning_group_projects')
    op.drop_table('learning_group_students')
    op.drop_table('learning_group_teachers')
    op.drop_table('school_user_role')
    op.drop_table('school_role_permission')
    op.drop_table('school_role')
    op.drop_table('learning_group')
    # ### end Alembic commands ###