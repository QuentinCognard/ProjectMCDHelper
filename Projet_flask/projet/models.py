from .app import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    prenomU = db.Column(db.String(100))
    nomU = db.Column(db.String(100))
    loginU = db.Column(db.String(100))
    passwordU = db.Column(db.String(100))
    mailU = db.Column(db.String(100))

class Projet(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100))
    nameMCD=db.Column(db.String(100))
    description=db.Column(db.String(150))

def get_idmax():
    req = """SELECT max(idProjet) FROM PROJET"""
    avg = db.engine.execute(req).first()
    return avg

def get_user(login):
    User = User.query.filter(User.login==login).all()
    return User
