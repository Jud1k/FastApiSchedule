"""some fix

Revision ID: 5f01758a8c1b
Revises: 
Create Date: 2025-03-29 15:57:59.695938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f01758a8c1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('course', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('teachers')
    op.drop_table('subjects')
    op.drop_table('rooms')
    op.drop_table('groups')
    # ### end Alembic commands ###
