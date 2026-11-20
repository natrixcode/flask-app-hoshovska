from tinydb import TinyDB, Query
from flask import current_app


def get_table():
    db = TinyDB(current_app.config["DATA_PATH"], ensure_ascii=False, indent=2)
    return db, db.table("products")


def get_product(product_id):
    db, table = get_table()
    try:
        return table.get(Query().id == product_id)
    finally:
        db.close()
