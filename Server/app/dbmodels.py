from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    def __repr__(self):
        return '<User: {}>, <Email: {}>, <ID: {}>, <Pass-Hash: {}'.format(self.username, self.email, self.id, self.password)
        
# class Issues(db.Model):
#     pass
