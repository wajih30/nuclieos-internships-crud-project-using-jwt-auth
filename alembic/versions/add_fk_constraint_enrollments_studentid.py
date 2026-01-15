"""Add FK constraint to Enrollments.StudentId

Revision ID: add_fk_enrollments_studentid
Revises: b255a2d1e848
Create Date: 2026-01-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_fk_enrollments_studentid'
down_revision: Union[str, Sequence[str], None] = 'b255a2d1e848'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add FK constraint."""
    # Add foreign key constraint from Enrollments.StudentId to Users.id
    op.create_foreign_key(
        'fk_enrollments_studentid_users_id',
        'Enrollments',
        'Users',
        ['StudentId'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema - drop FK constraint."""
    op.drop_constraint('fk_enrollments_studentid_users_id', 'Enrollments', type_='foreignkey')
