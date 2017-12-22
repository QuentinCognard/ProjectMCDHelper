from .app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    prenomU = db.Column(db.String(100))
    nomU = db.Column(db.String(100))
    loginU = db.Column(db.String(100))
    passwordU = db.Column(db.String(100))
    mailU = db.Column(db.String(100))

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomProj = db.Column(db.String(100))
    nomMCD = db.Column(db.String(100))
    descProj = db.Column(db.String(500))

def get_user(login):
    User = User.query.filter(User.login==login).all()
    return User

def get_proj(idProj):
    projet = Projet.query.filter(Projet.id==idProj).all()
    return projet
