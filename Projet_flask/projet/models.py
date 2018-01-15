from .app import *
from flask_login import UserMixin
from sqlalchemy import func

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

class Droit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomDroit = db.Column(db.String(100))
    descDroit = db.Column(db.String(500))


class Gerer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"))
    user_login = db.Column(db.Integer, db.ForeignKey("user.login"))
    droit_id = db.Column(db.Integer, db.ForeignKey("droit.id"))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetGerer", lazy="dynamic"))
    user = db.relationship("User", foreign_keys=[user_login], backref=db.backref("userGerer", lazy="dynamic"))
    droit = db.relationship("Droit", foreign_keys=[droit_id], backref=db.backref("droitGerer", lazy="dynamic"))


class Entite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key = True)
    nomEntite = db.Column(db.String(100))
    positionEntite = db.Column(db.String(100))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetEntite", lazy="dynamic"))


class Attributs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    entite_id = db.Column(db.Integer, db.ForeignKey("entite.id"), primary_key=True)
    nomAttribut = db.Column(db.String(100))
    genreAttribut = db.Column(db.String(100))
    typeAttribut = db.Column(db.String(100))
    valeurAttribut = db.Column(db.String(100))
    actifAttribut = db.Column(db.String(100))
    entite = db.relationship("Entite", foreign_keys=[entite_id], backref=db.backref("projetEntite", lazy="dynamic"))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetAttribut", lazy="dynamic"))


class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    nomRelation = db.Column(db.String(100))
    positionRelation = db.Column(db.String(100))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetRelationn", lazy="dynamic"))

class RelationEntite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entite_id = db.Column(db.Integer, db.ForeignKey("entite.id"), primary_key=True)
    entite = db.relationship("Entite", foreign_keys=[entite_id], backref=db.backref("relationEntite", lazy="dynamic"))
    cardinaliteRelation = db.Column(db.String(100))

def get_user(login):
    User = User.query.filter(User.login==login).all()
    return User

def get_proj(idProj):
    projet = Projet.query.filter(Projet.id==idProj).all()
    return projet

@login_manager.user_loader
def load_user(login):
    return User.query.get(login)
