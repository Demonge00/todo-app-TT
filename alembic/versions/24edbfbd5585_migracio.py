"""migracio

Revision ID: 24edbfbd5585
Revises: 2fa3e0953996
Create Date: 2025-09-05 11:21:52.932832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24edbfbd5585'
down_revision: Union[str, Sequence[str], None] = '2fa3e0953996'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
