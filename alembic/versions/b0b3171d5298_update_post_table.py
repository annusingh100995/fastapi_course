"""update_post_table

Revision ID: b0b3171d5298
Revises: 8ae66ff060c2
Create Date: 2023-06-26 17:28:43.863699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0b3171d5298'
down_revision = '8ae66ff060c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
                                server_default=sa.text('NOW()')) )
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
