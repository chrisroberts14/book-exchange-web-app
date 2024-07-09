# pylint: skip-file
"""Add login.

Revision ID: 0108e7e0b5da
Revises: 42d4e4f06306
Create Date: 2024-07-09 16:28:42.546130
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0108e7e0b5da"
down_revision: Union[str, None] = "42d4e4f06306"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "new_users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=False, unique=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        "INSERT INTO new_users (id, username, email) SELECT id, username, email FROM users"
    )
    op.drop_table("users")
    op.rename_table("new_users", "users")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.create_table(
        "old_users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        "INSERT INTO old_users (id, username, email) SELECT id, username, email FROM users"
    )
    op.drop_table("users")
    op.rename_table("old_users", "users")
    # ### end Alembic commands ###
