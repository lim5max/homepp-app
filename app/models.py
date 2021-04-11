from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100), )
    username = db.Column(db.String(1000), unique=True, index=True)
    rbpi_secret_key = db.Column(db.String(20), unique=True, index=True)

    # def __init__(self, email, name, password):
    #     self.name = name
    #     self.email = email
    #     self.password = password

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))