from .app import *
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime

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
    mcd_textuel = db.Column(db.String(500))

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

    def __repr__(self):
        return "{};{};{};{}".format(self.id,self.projet_id,self.nomEntite,self.positionEntite)

class Attributs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    entite_id = db.Column(db.Integer, db.ForeignKey("entite.id"))
    nomAttribut = db.Column(db.String(100))
    genreAttribut = db.Column(db.String(100))
    typeAttribut = db.Column(db.String(100))
    primaryKey = db.Column(db.Boolean)
    entite = db.relationship("Entite", foreign_keys=[entite_id], backref=db.backref("projetEntite", lazy="dynamic"))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetAttribut", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{};{};{};{};{}".format(self.id,self.projet_id,self.entite_id,self.nomAttribut,self.genreAttribut,self.typeAttribut,self.actifAttribut)

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    nomRelation = db.Column(db.String(100))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetRelationn", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{}".format(self.id,self.projet_id,self.nomRelation)

class Relationentite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relation_id = db.Column(db.Integer, db.ForeignKey("relation.id"), primary_key=True)
    relation = db.relationship("Relation", foreign_keys=[relation_id], backref=db.backref("relationid", lazy="dynamic"))
    entite_id = db.Column(db.Integer, db.ForeignKey("entite.id"), primary_key=True)
    cardinaliteE = db.Column(db.String(100))
    entite = db.relationship("Entite", foreign_keys=[entite_id], backref=db.backref("Entite", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{};{};{}".format(self.id,self.relation_id,self.entite_id,self.cardinaliteE,self.cardinaliteR)

class Relationattributs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    relation_id = db.Column(db.Integer, db.ForeignKey("relation.id"), primary_key=True)
    relation = db.relationship("Relation", foreign_keys=[relation_id], backref=db.backref("relationattid", lazy="dynamic"))
    attribut_id = db.Column(db.Integer, db.ForeignKey("attributs.id"), primary_key=True)
    attributs = db.relationship("Attributs", foreign_keys=[attribut_id], backref=db.backref("attributid", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{};{}".format(self.id,self.relation_id,self.relation,self.attribut_id)


def get_tout_du_projet(idprojet):
    liste = []
    listeE = Entite.query.filter(Entite.projet_id==idprojet).all()
    listeA = Attributs.query.filter(Attributs.projet_id==idprojet).all()
    listeR = Relation.query.filter(Relation.projet_id==idprojet).all()
    listeRE = []
    listeRA = []
    for r in listeR:
        listeRE.append(Relationentite.query.filter(Relationentite.relation==r).all())
        listeRA.append(Relationattributs.query.filter(Relationattributs.relation==r).all())
    liste.append(listeE)
    liste.append(listeA)
    liste.append(listeR)
    liste.append(listeRE)
    liste.append(listeRA)
    return liste

class Notification(db.Model):
    nom= db.Column(db.Integer, primary_key=True)
    expediteur=db.Column(db.String(100),db.ForeignKey("user.login"),primary_key=True)
    destinataire=db.Column(db.String(100),db.ForeignKey("user.login"),primary_key=True)
    idProj=db.Column(db.Integer,db.ForeignKey("projet.id"), primary_key=True)
    texte=db.Column(db.String(300))
    date=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)


def get_nb_notifications(nom):
    return len(Notification.query.filter(Notification.destinataire==nom).all())

def get_notifications(nom):
    return Notification.query.filter(Notification.destinataire==nom).order_by(Notification.date.desc()).all()

def get_user(login):
    User = User.query.filter(User.login==login).all()
    return User

def get_proj(idProj):
    projet = Projet.query.filter(Projet.id==idProj).all()
    return projet

def get_nbid_entity():
    req = db.session.query(db.func.count(Entite.id)).scalar()
    return req

def get_nbid_attribut():
    req = db.session.query(db.func.count(Attributs.id)).scalar()
    return req

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

def get_projet_user(username,n):
    p= Projet.query.join(Gerer).filter(Gerer.user_login==username).all()
    res=[]
    indice=0
    if len(p)<n*5-1:
        indice=len(p)
    else:
        indice=n*5-1
    if n==1:
        start=(n-1)*5
    else:
        start=(n-1)*5-1
    for i in range(start,indice):
        res.append(p[i])
    return res

def get_projet(username, idProj):
    projets = Projet.query.join(Gerer).filter(Gerer.user_login==username).all()
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

def get_all_projets(n):
    p=Projet.query.all()
    res=[]
    indice=0
    if len(p)<n*5-1:
        indice=len(p)
    else:
        indice=n*5-n
    if n==1:
        start=(n-1)*5
    else:
        start=(n-1)*5-(n-1)
    for i in range(start,indice):
        res.append(p[i])
    return res

def get_attributs_projet(idProj):
    allatt= Attributs.query.join(Projet).filter(Projet.id==idProj).all()
    res=[]
    for elem in allatt:
        res.append(elem)
    return res


def get_user_projet(nomProj):
    gerer=get_gerer_byProjet(nomProj)
    res=[]
    for g in gerer:
        res.append(g.user_login)
    return res


def get_attributs_proj(idProj):
    return Attributs.query.filter(Attributs.projet_id == idProj).all()

def get_master_proj(nomProj):
    projet=get_gerer_byProjet(nomProj)
    for p in projet:
        if p.droit_id==1:
            return p.user_login
    return None


def get_notif_byexp_dest_id(exp,dest,id):
    return Notification.query.filter(Notification.expediteur==exp,Notification.destinataire==dest,Notification.idProj==id).first()

def get_notif_byexp_dest_nom(nom,exp,dest,id):
    return Notification.query.filter(Notification.nom==nom,Notification.expediteur==exp,Notification.destinataire==dest,Notification.idProj==id).all()


def test(test):
     return db.session.query(Projet).filter(Projet.nomProj.like("%" + test + "%")).all()

def get_entity(idProj):
    return Entite.query.filter(Entite.projet_id == idProj).all()

def get_entitybyname(idProj,nom):
    return Entite.query.filter(Entite.projet_id == idProj,Entite.nomEntite==nom).first()

def getattributbyname(idProj,nom):
    return Attributs.query.filter(Attributs.projet_id == idProj,Attributs.nomAttribut==nom).first()

def getrelations(idProj):
    return Relation.query.filter(Relation.projet_id== idProj).all()

def getrelationsentites():
    return Relationentite.query.all()

def getrelationsattributs(idProj):
    return Relationattributs.query.filter(Relationattributs.projet_id==idProj).all()

def get_relAtt_byProjRel(idProj, idRel):
    return Relationattributs.query.filter(Relationattributs.projet_id==idProj).filter(Relationattributs.relation_id==idRel).all()

def get_entityrel_byIdRel(idRel):
    return Relationentite.query.filter(Relationentite.relation_id==idRel).all()

def get_relation_byId(idRel, idProj):
    return Relation.query.filter(Relation.id == idRel).filter(Relation.projet_id == idProj).one()

def get_relAtt_byAtt(attId, idProj):
    return Relationattributs.query.filter(Relationattributs.attribut_id == attId).filter(Relationattributs.projet_id == idProj).all()
