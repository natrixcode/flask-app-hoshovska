"""Insert data into products table

Revision ID: 36b84c0c6b41
Revises: c5e1b5f35abe
Create Date: 2026-11-19 11:51:51.786674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36b84c0c6b41'
down_revision = 'c5e1b5f35abe'
branch_labels = None
depends_on = None


def upgrade():
    """Додати категорії та продукти."""
    categories_table = sa.table(
        "categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    products_table = sa.table(
        "products",
        sa.column("name", sa.String),
        sa.column("price", sa.Float),
        sa.column("active", sa.Boolean),
        sa.column("category_id", sa.Integer),
    )

    connection = op.get_bind()

    categories = [
        "Electronics",
        "Books",
        "Clothing",
    ]

    op.bulk_insert(
        categories_table,
        [{"name": name} for name in categories],
    )

    rows = connection.execute(
        sa.select(
            categories_table.c.id,
            categories_table.c.name,
        ).where(
            categories_table.c.name.in_(categories)
        )
    ).all()

    category_ids = {
        row.name: row.id
        for row in rows
    }

    op.bulk_insert(
        products_table,
        [
            {
                "name": "Laptop",
                "price": 1200.0,
                "active": True,
                "category_id": category_ids["Electronics"],
            },
            {
                "name": "Smartphone LG",
                "price": 800.0,
                "active": True,
                "category_id": category_ids["Electronics"],
            },
            {
                "name": "Novel",
                "price": 20.0,
                "active": True,
                "category_id": category_ids["Books"],
            },
            {
                "name": "T-Shirt",
                "price": 25.0,
                "active": False,
                "category_id": category_ids["Clothing"],
            },
        ],
    )


def downgrade():
    """Видалити дані, додані цією міграцією."""
    connection = op.get_bind()

    connection.execute(
        sa.text(
            "DELETE FROM products "
            "WHERE name IN "
            "('Laptop', 'Smartphone LG', "
            "'Novel', 'T-Shirt')"
        )
    )

    connection.execute(
        sa.text(
            "DELETE FROM categories "
            "WHERE name IN "
            "('Electronics', 'Books', 'Clothing')"
        )
    )
