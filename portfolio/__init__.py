from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Myportfolioproject1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Telegram bot configuration
    app.config['TELEGRAM_BOT_TOKEN'] = '7433541289:AAGWNYj7hct-clPALUElTNZAe0vfDMHVTNs'
    app.config['TELEGRAM_CHAT_ID'] = '1517989742'

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    with app.app_context():
        db.create_all()
    
    return app
