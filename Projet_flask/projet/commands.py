from .app import manager, db
import yaml
from .models import *
from hashlib import sha256

@manager.command
def syncdb():
    db.create_all()

@manager.command
def newuser(login, password):
    m = sha256()
    m.update(password.encode())
    u = User(prenom = None, nom = None, login=login, password = m.hexdigest())
    db.session.add(u)
    db.session.commit()

@manager.command
def loaddroit(filename):
    db.create_all()
    droits = yaml.load(open(filename))
    for d in droits:
        o = Droit(nomDroit=d["nomDroit"],descDroit=d["DescDroit"])
        db.session.add(o)
    db.session.commit()

@manager.command
def loadprojet(filename):
    db.create_all()
    projets = yaml.load(open(filename))
    for p in projets:
        o = Projet(nomProj=p["nomProjet"],nomMCD=p["nomMcd"],descProj=p["DescProjet"])
        db.session.add(o)
    db.session.commit()

@manager.command
def loadgerer(filename):
    db.create_all()
    gerer = yaml.load(open(filename))
    for g in gerer:
        o = Gerer(projet_id=g["idProjet"],user_login=g["idUser"],droit_id=g["idDroit"])
        db.session.add(o)
    db.session.commit()
