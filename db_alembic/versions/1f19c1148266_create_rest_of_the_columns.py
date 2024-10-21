"""create rest of the  columns

Revision ID: 1f19c1148266
Revises: 28bce20e3ce4
Create Date: 2024-10-21 20:45:40.594896

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f19c1148266"
down_revision: Union[str, None] = "28bce20e3ce4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=True))
    op.add_column("posts", sa.Column("rating", sa.Float(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "rating")
    op.drop_column("posts", "published")
    pass
