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
        o = Projet(nomProj=p["nomProjet"],mcd_textuel = p["mcd_textuel"],nomMCD=p["nomMcd"],descProj=p["DescProjet"])
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


@manager.command
def loadentite(filename):
    db.create_all()
    entite = yaml.load(open(filename))
    for e in entite:
        o = Entite(id=e["id"],projet_id=e["projet_id"],nomEntite=e["nomEntite"])
        db.session.add(o)
    db.session.commit()

@manager.command
def loadrelation(filename):
    db.create_all()
    relation = yaml.load(open(filename))
    for r in relation:
        o = Relation(id=r["id"],id_relationEntite = r["id_relationEntite"],projet_id=r["projet_id"],nomRelation=r["nomrelation"],entite1_id=r["entite1_id"],entite2_id=r["entite2_id"],cardinalite1=r["cardinalite1"],cardinalite2=r["cardinalite2"])
        db.session.add(o)
    db.session.commit()

@manager.command
def loadattributs(filename):
    db.create_all()
    attributs = yaml.load(open(filename))
    for a in attributs:
        o = Attributs(id=a["id"],projet_id=a["projet_id"],entite_id=a["entite_id"],nomAttribut=a["nomAttribut"],genreAttribut=a["genreAttribut"],typeAttribut=a["typeAttribut"],valeurAttribut=a["valeurAttribut"])
        db.session.add(o)
    db.session.commit()
