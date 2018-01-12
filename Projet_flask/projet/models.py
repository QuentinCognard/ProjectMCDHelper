from .app import *
from flask_login import UserMixin

class User(db.Model, UserMixin):
    prenom = db.Column(db.String(100))
    nom = db.Column(db.String(100))
    login = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    mail = db.Column(db.String(100))

    def get_id(self):
        return self.login

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

@login_manager.user_loader
def load_user(login):
    return User.query.get(login)
