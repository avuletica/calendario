"""add calendar & calendar entry tables

Revision ID: 2a389d7dd600
Revises: 4e0c9efe396b
Create Date: 2020-11-28 17:28:05.542682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a389d7dd600"
down_revision = "4e0c9efe396b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "apartment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("owner_id", "name", name="unique_owner_id_name"),
    )
    op.create_table(
        "apartment_calendar",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file", sa.LargeBinary(), nullable=False),
        sa.Column("import_url", sa.String(), nullable=True),
        sa.Column("apartment_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["apartment_id"],
            ["apartment.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("apartment_id", name="unique_apartment_id"),
    )
    op.create_table(
        "apartment_calendar_entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("summary", sa.String(length=128), nullable=True),
        sa.Column("start_datetime", sa.DateTime(), nullable=False),
        sa.Column("end_datetime", sa.DateTime(), nullable=False),
        sa.Column("apartment_calendar_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["apartment_calendar_id"],
            ["apartment_calendar.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("apartment_calendar_entry")
    op.drop_table("apartment_calendar")
    op.drop_table("apartment")
    # ### end Alembic commands ###
