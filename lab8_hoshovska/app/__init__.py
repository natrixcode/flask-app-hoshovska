from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import os
from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name=None):
    app = Flask(__name__)
    from app.config import CONFIGS

    name = config_name or os.getenv("FLASK_CONFIG", "development")
    if name not in CONFIGS:
        raise ValueError(f"Unknown configuration: {name}")
    app.config.from_object(CONFIGS[name])
    if name == "production" and not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY is required in production")
    db.init_app(app)
    from app.users.models import User
    from app.posts.models import Post, Tag

    migrate.init_app(app, db)
    csrf.init_app(app)
    from app.posts import post_bp

    app.register_blueprint(post_bp)

    @app.route("/")
    def home():
        return redirect(url_for("posts.all_posts"))

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app
