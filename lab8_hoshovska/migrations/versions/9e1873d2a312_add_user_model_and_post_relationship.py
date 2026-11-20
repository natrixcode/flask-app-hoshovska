"""Add User model and Post relationship.

Revision ID: 9e1873d2a312
Revises: 13577b217442
"""

from alembic import op
import sqlalchemy as sa

revision = "9e1873d2a312"
down_revision = "13577b217442"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    inspector = sa.inspect(connection)

    tables = inspector.get_table_names()

    if "user" not in tables:
        op.create_table(
            "user",
            sa.Column(
                "id",
                sa.Integer(),
                primary_key=True,
            ),
            sa.Column(
                "username",
                sa.String(length=80),
                nullable=False,
                unique=True,
            ),
        )

    post_columns = {column["name"] for column in inspector.get_columns("post")}

    if "user_id" not in post_columns:
        with op.batch_alter_table("post") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "user_id",
                    sa.Integer(),
                    nullable=True,
                )
            )

    inspector = sa.inspect(connection)

    foreign_keys = inspector.get_foreign_keys("post")

    has_user_foreign_key = any(
        foreign_key["constrained_columns"] == ["user_id"]
        and foreign_key["referred_table"] == "user"
        for foreign_key in foreign_keys
    )

    if not has_user_foreign_key:
        with op.batch_alter_table("post") as batch_op:
            batch_op.create_foreign_key(
                "fk_post_user_id",
                "user",
                ["user_id"],
                ["id"],
            )


def downgrade():
    with op.batch_alter_table("post") as batch_op:
        batch_op.drop_constraint(
            "fk_post_user_id",
            type_="foreignkey",
        )

        batch_op.drop_column("user_id")

    op.drop_table("user")
