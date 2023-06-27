"""add_content_to_post

Revision ID: 848f35a6819c
Revises: 4188619ee96c
Create Date: 2023-06-26 16:53:58.987309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '848f35a6819c'
down_revision = '4188619ee96c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
