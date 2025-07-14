from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from datetime import datetime


db = SQLAlchemy()

login_manager = LoginManager()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'devkey'

    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

    db.init_app(app)

    login_manager.init_app(app)
    
    bcrypt.init_app(app)

    from app.routes import app as routes_blueprint 

    app.register_blueprint(routes_blueprint)

    with app.app_context():
        db.create_all()

    return app 

