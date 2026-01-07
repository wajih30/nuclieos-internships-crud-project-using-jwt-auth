"""corrected column type from string to integer of tables quizzes, quizscore and lessons

Revision ID: 9dfe740e36a3
Revises: be06ee42ea1a
Create Date: 2025-12-26 14:36:44.641667
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9dfe740e36a3'
down_revision: Union[str, Sequence[str], None] = 'be06ee42ea1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Lessons table
    op.alter_column(
        'Lessons',
        'InstructorId',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using='"InstructorId"::integer'
    )

    # QuizScore table
    op.alter_column(
        'QuizScore',
        'InstructorId',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using='"InstructorId"::integer'
    )

    # Quizzes table
    op.alter_column(
        'Quizzes',
        'InstructorId',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using='"InstructorId"::integer'
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Lessons table
    op.alter_column(
        'Lessons',
        'InstructorId',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using='"InstructorId"::varchar'
    )

    # QuizScore table
    op.alter_column(
        'QuizScore',
        'InstructorId',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using='"InstructorId"::varchar'
    )

    # Quizzes table
    op.alter_column(
        'Quizzes',
        'InstructorId',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using='"InstructorId"::varchar'
    )
