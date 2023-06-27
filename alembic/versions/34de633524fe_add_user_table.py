"""add_user_table

Revision ID: 34de633524fe
Revises: 848f35a6819c
Create Date: 2023-06-26 16:59:20.681027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34de633524fe'
down_revision = '848f35a6819c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                              sa.PrimaryKeyConstraint('id'),
                              sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
