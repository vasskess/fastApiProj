"""testing wrong field

Revision ID: 8ceb9c6a94f0
Revises: c80343c594eb
Create Date: 2024-10-21 21:08:35.203679

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8ceb9c6a94f0"
down_revision: Union[str, None] = "c80343c594eb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("author", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("posts", "author")
    pass
