"""initial

Revision ID: f61eb5e12e0f
Revises:
Create Date: 2022-06-20 13:06:43.058884

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f61eb5e12e0f'
down_revision = None
branch_labels = None
depends_on = None

node_type = sa.Enum('OFFER', 'CATEGORY', name='node_type')


def upgrade():
    op.create_table(
        'nodes',
        sa.Column('uuid', postgresql.UUID(), nullable=False),
        sa.Column('node_type', node_type, nullable=False),
        sa.Column('parent_uuid', postgresql.UUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk__nodes'))
    )


def downgrade():
    op.drop_table('nodes')
    node_type.drop(op.get_bind())
