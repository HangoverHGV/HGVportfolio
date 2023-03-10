import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .keygen import generatepass


load_dotenv()


db = SQLAlchemy()

db_user = os.getenv('USER')
db_name = os.getenv('DATABASE')
db_password = os.getenv('PASSWORD')
db_host = os.getenv('HOST')
uri = 'mysql+pymysql://' + str(db_user) + ':' + str(db_password) + '@' + str(db_host) + '/' + str(db_name)

def create_app():
    app = Flask(__name__)
    app.secret_key = generatepass()
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from website import models

    with app.app_context():
        db.create_all()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from website.models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
