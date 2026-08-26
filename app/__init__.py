from flask import Flask

from config.config import Config
from app.routes.health import health_bp
from app.routes.chat import chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(health_bp)
    app.register_blueprint(chat_bp)

    return app