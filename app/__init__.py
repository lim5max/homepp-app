from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask import Flask, render_template, redirect, request, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
#Конфигурация
from flask_migrate import Migrate

login = LoginManager()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
def create_app(config_class = Config):
    #Инициализация
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    db.init_app(app)
    #csrf.init_app(app)
    login.init_app(app)
    
    csrf.init_app(app)
    

    from .models import User
    with app.app_context():
        db.drop_all()
        db.create_all()
        u = User(username='admin')
        u.set_password('neqwerty')
        db.session.add(u)
        db.session.commit()


    migrate = Migrate(app, db)
    CORS(app)
    cors = CORS(app,
        resources={
            r"/*": {
                "origins": "*" # localhost:5000, 0.0.0.0:5000
            }
    })
    from . import auth
    app.register_blueprint(auth.auth)

    login.login_view = 'auth.login'
    #Обработка ошибок
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
