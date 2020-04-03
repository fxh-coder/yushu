from flask import Flask
# from app.models.user import User
from flask_login import LoginManager
from app.models.book import db
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()

# @login_manager.user_loader
# def load_user(userid):
#     return User.query.get(userid)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    mail.init_app(app)

    with app.app_context():
        db.create_all()
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
