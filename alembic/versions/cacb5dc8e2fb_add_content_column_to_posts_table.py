"""add content column to posts table

Revision ID: cacb5dc8e2fb
Revises: 8c925bf48f03
Create Date: 2023-07-14 16:04:46.355020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cacb5dc8e2fb'
down_revision = '8c925bf48f03'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')  
    pass
