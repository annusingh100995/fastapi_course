"""create_post_table

Revision ID: 4188619ee96c
Revises: 
Create Date: 2023-06-26 16:39:22.281381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4188619ee96c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
