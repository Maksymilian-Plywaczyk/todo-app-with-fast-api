"""create user table

Revision ID: 9db4bc286def
Revises:
Create Date: 2022-11-30 18:28:36.558101

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9db4bc286def"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(), index=True),
        sa.Column("email", sa.String(), unique=True, index=True, nullable=False),
        sa.Column("hashed_password", sa.String()),
        sa.Column("is_active", sa.Boolean(), default=True),
    )


def downgrade() -> None:
    op.drop_table("users")
