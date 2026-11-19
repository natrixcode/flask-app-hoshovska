from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": (
                "fk_%(table_name)s_%(column_0_name)s_"
                "%(referred_table_name)s"
            ),
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    project_dir = Path(__file__).resolve().parent.parent
    database_path = project_dir / "instance" / "lab7.sqlite"

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    app.config.update(
        SECRET_KEY="lab7-development-only",
        SQLALCHEMY_DATABASE_URI=(
            f"sqlite:///{database_path}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from app.products import products_bp
    from app.products import models

    app.register_blueprint(products_bp)

    return app
