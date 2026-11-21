from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import os
from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
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
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    login_manager.login_message = "Для доступу до сторінки увійдіть у систему."
    login_manager.login_message_category = "warning"
    from app.users.models import User
    from app.posts.models import Post, Tag

    migrate.init_app(app, db)
    csrf.init_app(app)
    from app.posts import post_bp

    app.register_blueprint(post_bp)

    from app.users.routes import users_bp
    app.register_blueprint(users_bp)

    @app.route("/")
    def home():
        return redirect(url_for("posts.all_posts"))

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app



@login_manager.user_loader
def load_user(user_id):
    from app.users.models import User

    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
