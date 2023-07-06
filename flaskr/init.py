from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple','CACHE_DEFAULT_TIMEOUT': 86400})

def create_app():

    application =Flask(__name__)
    cache.init_app(application)

    application.config['SECRET_KEY'] = "secret-key"
    application.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.db')
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(application)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    application.register_blueprint(auth_blueprint)

    return application

app = create_app()
# if __name__ == "__main__":
#     app = create_app()
#     app.run()