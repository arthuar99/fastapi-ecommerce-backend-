"""init

Revision ID: 20250901_000001
Revises: 
Create Date: 2025-09-01 00:00:01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250901_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('user', 'admin', name='role'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')), 
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('image', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.create_index('ix_products_name', 'products', ['name'], unique=True)

    # carts table
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_carts_id', 'carts', ['id'], unique=False)
    op.create_unique_constraint('uq_carts_user_id', 'carts', ['user_id'])

    # cart_items table
    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cart_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['cart_id'], ['carts.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_cart_items_id', 'cart_items', ['id'], unique=False)
    op.create_unique_constraint('uq_cart_product', 'cart_items', ['cart_id', 'product_id'])


def downgrade() -> None:
    op.drop_constraint('uq_cart_product', 'cart_items', type_='unique')
    op.drop_index('ix_cart_items_id', table_name='cart_items')
    op.drop_table('cart_items')

    op.drop_constraint('uq_carts_user_id', 'carts', type_='unique')
    op.drop_index('ix_carts_id', table_name='carts')
    op.drop_table('carts')

    op.drop_index('ix_products_name', table_name='products')
    op.drop_index('ix_products_id', table_name='products')
    op.drop_table('products')

    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')


