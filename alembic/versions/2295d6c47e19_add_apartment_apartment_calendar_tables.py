"""add apartment & apartment calendar tables

Revision ID: 2295d6c47e19
Revises: 4e0c9efe396b
Create Date: 2020-11-26 19:51:24.443764

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2295d6c47e19'
down_revision = '4e0c9efe396b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apartment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id', 'name', name='unique_id_name')
    )
    op.create_table('apartment_calendar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summary', sa.String(length=128), nullable=True),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('ics_file', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('apartment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apartment_id'], ['apartment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apartment_calendar')
    op.drop_table('apartment')
    # ### end Alembic commands ###
