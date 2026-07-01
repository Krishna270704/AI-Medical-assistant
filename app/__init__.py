import logging
import os
from flask import Flask
from dotenv import load_dotenv
from app.core.config import Config
from app.models import db
from flask_login import LoginManager
from flask_migrate import Migrate

from logging.handlers import RotatingFileHandler

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def setup_logging():
    os.makedirs('data/logs', exist_ok=True)
    os.makedirs('data/uploads', exist_ok=True)
    os.makedirs('data/audio', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('data/logs/app.log', maxBytes=1000000, backupCount=5),
            logging.StreamHandler()
        ]
    )

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging()
    app.logger.info('Medical Assistant startup')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    
    # Initialize Security (Limiter and Talisman)
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from flask_talisman import Talisman

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    # Disable HTTPS redirect in dev, enable CSP securely
    csp = {
        'default-src': [
            '\'self\'',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com',
        ],
        'script-src': [
            '\'self\'',
            '\'unsafe-inline\'', # Required for inline SSE fetch script
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'https://fonts.googleapis.com',
        ],
        'media-src': ['\'self\'', 'blob:']
    }
    # Detect Railway environment
    is_railway = bool(os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_PROJECT_ID'))
    # Force HTTPS only if secure cookies are enabled AND we are not on Railway
    force_https = app.config.get('SESSION_COOKIE_SECURE', False) and not is_railway
    
    Talisman(app, content_security_policy=csp, force_https=force_https)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
        
    # Validate LLM Provider configuration
    if app.config.get('LLM_PROVIDER') == 'nvidia' and not app.config.get('NVIDIA_API_KEY'):
        app.logger.warning("NVIDIA_API_KEY is not set. NVIDIA API calls will fail.")
        
    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.monitoring import monitoring_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(monitoring_bp)

    return app
