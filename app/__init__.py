from flask import Flask
from .extensions import db, login_manager, socketio, mail
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # set config file

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    # Import models AFTER extensions are initialized to avoid circular imports
    from app.models import User, StudyRoom

    # Setup user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Load env
    from dotenv import load_dotenv
    load_dotenv()

    # Register Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.studyroom import studyroom_bp
    app.register_blueprint(studyroom_bp, url_prefix='/studyroom')

    try:
        from app.main import main_bp # Register main Blueprint
        app.register_blueprint(main_bp)
    except ImportError:
        pass  
    
    from app import sockets
    return app
    
