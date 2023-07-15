"""add foreign-key to post table

Revision ID: dd1cab3a02e8
Revises: e2af107e1229
Create Date: 2023-07-14 17:15:43.034295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd1cab3a02e8'
down_revision = 'e2af107e1229'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    # ORDER MATTERS HERE, must drop fk first then column
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
