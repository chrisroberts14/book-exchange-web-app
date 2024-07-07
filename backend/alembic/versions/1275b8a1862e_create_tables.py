# pylint: skip-file
"""Create tables.

Revision ID: 1275b8a1862e
Revises:
Create Date: 2024-07-07 14:50:21.432796
"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "1275b8a1862e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade the database.

    :return:
    """


def downgrade() -> None:
    """
    Downgrade the database.

    :return:
    """
