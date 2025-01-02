"""Add avatar column to ChatMessage

Revision ID: d60786a905e4
Revises: 
Create Date: 2024-12-30 12:18:47.274651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd60786a905e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.String(length=50), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_message')
    # ### end Alembic commands ###
