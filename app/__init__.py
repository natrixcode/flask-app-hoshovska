from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../config.py')

app.config['SECRET_KEY'] = 'super-secret-key-for-lab4-hoshovska'

from app.users import user_bp
from app.products import products_bp

from app.auth.routes import auth_bp

app.register_blueprint(user_bp)
app.register_blueprint(products_bp)

app.register_blueprint(auth_bp, url_prefix='/auth')

from app import views