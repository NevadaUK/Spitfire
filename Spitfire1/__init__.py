from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from Spitfire1.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from Spitfire1.users.routes import users
    from Spitfire1.posts.routes import posts
    from Spitfire1.base.routes import base
    from Spitfire1.errors.handlers import errors
    from Spitfire1.dash.routes import dash
    from Spitfire1.groups.routes import groups

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(base)
    app.register_blueprint(errors)
    app.register_blueprint(dash)
    app.register_blueprint(groups)

    return app
