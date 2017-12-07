from .app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    prenomU = db.Column(db.String(100))
    nomU = db.Column(db.String(100))
    loginU = db.Column(db.String(100))
    passwordU = db.Column(db.String(100))
    mailU = db.Column(db.String(100))
