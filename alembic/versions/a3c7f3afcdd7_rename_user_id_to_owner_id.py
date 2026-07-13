"""rename user_id to owner_id

Revision ID: a3c7f3afcdd7
Revises: 50531f92702a
Create Date: 2026-07-13 09:39:10.519886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c7f3afcdd7'
down_revision: Union[str, Sequence[str], None] = '50531f92702a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "notes",
        "user_id",
        new_column_name="owner_id"
    )


def downgrade() -> None:
    op.alter_column(
        "notes",
        "owner_id",
        new_column_name="user_id"
    )
