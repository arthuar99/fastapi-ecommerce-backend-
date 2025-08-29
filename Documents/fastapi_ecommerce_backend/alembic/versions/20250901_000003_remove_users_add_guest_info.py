"""remove users add guest info

Revision ID: 20250901_000003
Revises: 20250901_000002
Create Date: 2025-09-01 00:00:03

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250901_000003'
down_revision = '20250901_000002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add guest information columns to orders
    op.add_column('orders', sa.Column('guest_name', sa.String(), nullable=False, server_default='Guest'))
    op.add_column('orders', sa.Column('guest_email', sa.String(), nullable=False, server_default='guest@example.com'))
    op.add_column('orders', sa.Column('guest_phone', sa.String(), nullable=False, server_default='000-000-0000'))


def downgrade() -> None:
    # Remove guest columns
    op.drop_column('orders', 'guest_phone')
    op.drop_column('orders', 'guest_email')
    op.drop_column('orders', 'guest_name')
