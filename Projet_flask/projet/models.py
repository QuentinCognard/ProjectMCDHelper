from .app import *
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    prenom = db.Column(db.String(100))
    nom = db.Column(db.String(100))
    login = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    image = db.Column(db.String(100))

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
    user_login = db.Column(db.String, db.ForeignKey("user.login"))
    droit_id = db.Column(db.Integer, db.ForeignKey("droit.id"))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetGerer", lazy="dynamic"))
    user = db.relationship("User", foreign_keys=[user_login], backref=db.backref("userGerer", lazy="dynamic"))
    droit = db.relationship("Droit", foreign_keys=[droit_id], backref=db.backref("droitGerer", lazy="dynamic"))

    def __init__(self,projet_id,user_login,droit_id):
        self.projet_id=projet_id
        self.user_login=user_login
        self.droit_id=droit_id

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

def get_all_login():
    users=User.query.all()
    res=[]
    for u in users:
        res.append((u.login,u.login))
    return res

def get_all_droit():
    droits=Droit.query.all()
    res=[]
    for d in droits:
        res.append((d.id,d.nomDroit))
    return res


def get_projet_user(username):
    return Projet.query.join(Gerer).filter(Gerer.user_login==username).all()

def get_projet(username, idProj):
    projets = get_projet_user(username)
    for p in projets:
        if p.id == idProj:
            return p
    return None

def get_Projet_byName(name):
    return Projet.query.filter(Projet.nomProj==name).first()

def get_gerer_byProjet(nomProj):
    return Gerer.query.join(Projet).filter(Projet.nomProj==nomProj).all()

def get_gerer_byNom(nomProj,nom):
    # print(Gerer.query.join(Projet).filter(Projet.nomProj==nomProj,Gerer.user_login==nom).all())
    return Gerer.query.join(Projet).filter(Projet.nomProj==nomProj,Gerer.user_login==nom).first()

def get_id_droit(nomDroit):
    return Droit.query.filter(Droit.nomDroit==nomDroit).first().id

def get_nom_droit(id):
    return Droit.query.filter(Droit.id==id).first().nomDroit

def get_all_projets():
    return Projet.query.all()
