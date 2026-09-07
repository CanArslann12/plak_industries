from flask import Flask, jsonify
from flask_cors import CORS

from config import get_config, validate_config


def create_app(config_object=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    config_class = config_object or get_config()
    validate_config(config_class)
    app.config.from_object(config_class)

    CORS(app, origins=app.config["CORS_ORIGINS"])

    from app.database import init_db
    from app.routes import api, pages

    init_db(app)
    app.register_blueprint(pages)
    app.register_blueprint(api)

    @app.get("/health")
    def health():
        return jsonify(basari=True, durum="ok")

    @app.errorhandler(Exception)
    def handle_unexpected_error(_error):
        return jsonify(basari=False, hata="Beklenmeyen bir sunucu hatası oluştu."), 500

    return app
