from flask import jsonify
from sqlalchemy import select

from app import db
from app.products import products_bp
from app.products.models import Product


@products_bp.get("/")
def list_products():
    products = db.session.scalars(
        select(Product).order_by(Product.id)
    ).all()

    return jsonify(
        [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
            }
            for product in products
        ]
    )
