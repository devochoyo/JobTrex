"""user role bug fixed

Revision ID: 5fbcbe9ca003
Revises: 7b33e8c3f917
Create Date: 2026-10-05 15:10:22.749734
"""

from alembic import op
import sqlalchemy as sa


revision = '5fbcbe9ca003'
down_revision = '7b33e8c3f917'
branch_labels = None
depends_on = None


def upgrade():
    userrole = sa.Enum(
        'ADMIN',
        'Employer',
        'APPLICANT',
        name='userrole'
    )

    userrole.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column('role', userrole, nullable=True)
    )

    op.execute(
        "UPDATE users SET role = 'APPLICANT' WHERE role IS NULL"
    )

    op.alter_column(
        'users',
        'role',
        nullable=False
    )


def downgrade():
    op.drop_column('users', 'role')

    userrole = sa.Enum(
        'ADMIN',
        'Employer',
        'APPLICANT',
        name='userrole'
    )

    userrole.drop(op.get_bind(), checkfirst=True)