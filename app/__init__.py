from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import models

    # Register the main Dashboard on the Root URL
    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Move the groceries app so it sits cleanly behind /groceries
    from app.groceries import groceries_bp
    app.register_blueprint(groceries_bp, url_prefix='/groceries')

    return app