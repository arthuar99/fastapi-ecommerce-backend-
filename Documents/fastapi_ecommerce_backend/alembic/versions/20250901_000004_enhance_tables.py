"""enhance tables

Revision ID: 20250901_000004
Revises: 20250901_000003
Create Date: 2025-09-01 00:00:04

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250901_000004'
down_revision = '20250901_000003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add status field to orders
    op.add_column('orders', sa.Column('status', sa.String(), nullable=False, server_default='pending'))
    
    # Add total_price and total_items to orders
    op.add_column('orders', sa.Column('total_price', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('orders', sa.Column('total_items', sa.Integer(), nullable=False, server_default='0'))
    
    # Add stock field to products
    op.add_column('products', sa.Column('stock', sa.Integer(), nullable=False, server_default='0'))
    
    # Add category field to products
    op.add_column('products', sa.Column('category', sa.String(), nullable=True))
    
    # Add is_active field to products
    op.add_column('products', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
    
    # Add session_id to carts for better session management
    op.add_column('carts', sa.Column('session_id', sa.String(), nullable=True))
    
    # Add created_at and updated_at to carts
    op.add_column('carts', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')))
    op.add_column('carts', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')))
    
    # Add created_at to cart_items
    op.add_column('cart_items', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')))


def downgrade() -> None:
    # Remove added columns
    op.drop_column('cart_items', 'created_at')
    op.drop_column('carts', 'updated_at')
    op.drop_column('carts', 'created_at')
    op.drop_column('carts', 'session_id')
    op.drop_column('products', 'is_active')
    op.drop_column('products', 'category')
    op.drop_column('products', 'stock')
    op.drop_column('orders', 'total_items')
    op.drop_column('orders', 'total_price')
    op.drop_column('orders', 'status')
