"""fix cart user_id

Revision ID: 20250901_000005
Revises: 20250901_000004
Create Date: 2025-09-01 00:00:05

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250901_000005'
down_revision = '20250901_000004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the user_id column from carts table if it exists
    try:
        op.drop_column('carts', 'user_id')
    except:
        pass  # Column might not exist


def downgrade() -> None:
    # Recreate user_id column
    try:
        op.add_column('carts', sa.Column('user_id', sa.Integer(), nullable=True))
    except:
        pass  # Column might already exist
