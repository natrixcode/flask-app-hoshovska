from pathlib import Path
from flask import Flask, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from config import Config


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    for key in ('DATA_PATH', 'CONTACT_LOG', 'UPLOAD_FOLDER'):
        Path(app.config[key]).parent.mkdir(parents=True, exist_ok=True)
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    from app.views import main
    from app.products.routes import products
    app.register_blueprint(main)
    app.register_blueprint(products)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(error):
        return render_template('413.html'), 413

    return app
