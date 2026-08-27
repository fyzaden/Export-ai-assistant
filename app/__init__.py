from flask import Flask
from flask_cors import CORS

from config.config import Config
from app.routes.health import health_bp
from app.routes.chat import chat_bp
from database.db import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    CORS(app)
    init_db()

    app.register_blueprint(health_bp)
    app.register_blueprint(chat_bp)

    return app