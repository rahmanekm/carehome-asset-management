from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main, auth, equipment
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(equipment.bp)

    # Add nl2br filter
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if s is None:
            return ''
        return s.replace('\n', '<br>')

    with app.app_context():
        db.create_all()

    return app 