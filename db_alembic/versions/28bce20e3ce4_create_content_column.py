"""create content column

Revision ID: 28bce20e3ce4
Revises: 9dede044fa1b
Create Date: 2024-10-21 20:40:22.684566

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "28bce20e3ce4"
down_revision: Union[str, None] = "9dede044fa1b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
