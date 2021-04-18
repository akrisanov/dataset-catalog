"""Create datasets table

Revision ID: 7b506e5952e7
Revises: 
Create Date: 2021-04-18 12:51:48.395398

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "7b506e5952e7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "datasets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True, comment="Name of the dataset"),
        sa.Column(
            "path",
            sa.Text(),
            nullable=False,
            comment="Relative path to the dataset inside object storage",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("datasets")
    # ### end Alembic commands ###