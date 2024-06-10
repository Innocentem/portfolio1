from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Initialize SQLAlchemy and Migrate instances
db = SQLAlchemy()
migrate = Migrate() 

def create_app():
    # Load environment variables from .env file
    load_dotenv('bots.env')

    # Create a new Flask application instance
    app = Flask(__name__)

    # Set application configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN')
    app.config['TELEGRAM_CHAT_ID'] = os.getenv('TELEGRAM_CHAT_ID')

    # Ensure the SQLALCHEMY_DATABASE_URI is set
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI must be set")

    # Initialize SQLAlchemy and Migrate with the app instance
    db.init_app(app)
    migrate.init_app(app, db) 

    # Register the main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register the auth blueprint with a URL prefix
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Create database tables within the app context
    with app.app_context():
        from .models import User, Item
        db.create_all()

    return app
