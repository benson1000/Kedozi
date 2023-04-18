from flask import Flask
from flask_bootstrap import Bootstrap
from os import path
from flask_login import LoginManager
import psycopg2
from . auth import *


def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@benso7130@kedozi"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = 'Thisisforkedozirealestatecompany'
    
    bootstrap = Bootstrap(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message_category = "info"
    
    @login_manager.user_loader
    def load_user(email):
        
        #making the query into the database
        conn = psycopg2.connect(user = "postgres",password = "@benso7130",  host = "localhost",  database = "kedozi")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        email = dict(session)['email']
        
        return user.email
    return app

