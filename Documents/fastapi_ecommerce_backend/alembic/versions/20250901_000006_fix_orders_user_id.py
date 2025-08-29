"""fix orders user_id

Revision ID: 20250901_000006
Revises: 20250901_000005
Create Date: 2025-09-01 00:00:06

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250901_000006'
down_revision = '20250901_000005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the user_id column from orders table if it exists
    try:
        op.drop_column('orders', 'user_id')
    except:
        pass  # Column might not exist


def downgrade() -> None:
    # Recreate user_id column
    try:
        op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=True))
    except:
        pass  # Column might already exist
