from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    # Load environment variables from bots.env file
    load_dotenv('bots.env')

    app = Flask(__name__)

    # Load configurations from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Telegram bot configuration
    app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN')
    app.config['TELEGRAM_CHAT_ID'] = os.getenv('TELEGRAM_CHAT_ID')

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI must be set")

    db.init_app(app)
    migrate.init_app(app, db)  # Integrate Flask-Migrate with the app and db

    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Import models to ensure they are registered
    with app.app_context():
        from .models import User, Item
        db.create_all()

    return app
