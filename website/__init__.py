import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .keygen import generatepass
from time import sleep
from sqlalchemy import inspect, create_engine

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





def create_database(app):
    from website import models
    rezultate_tbl = models.Rezultate().__class__.__name__
    user_tbl = models.User().__class__.__name__

    for i in range(6):
        connected = True
        try:
            db.session.execute('SELECT 1')
        except:
            connected = False

        if connected:
            break
        else:
            sleep(3)

    engine = create_engine(uri)

    def GetTableName(name):
        Exists = False
        tables = inspect(engine)
        for t_name in tables.get_table_names():
            if (t_name == name):
                Exists = True
                break
            else:
                Exists = False

        return Exists

    tables = []
    tables.append(GetTableName(rezultate_tbl))
    tables.append(GetTableName(user_tbl))

    result = all(tables)

    if not result:
        db.create_all(app=app)