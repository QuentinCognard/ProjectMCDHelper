from .app import *
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime


# Classe User contenant les infos sur les utilisateurs

class User(db.Model, UserMixin):
    prenom = db.Column(db.String(100))
    nom = db.Column(db.String(100))
    login = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    image = db.Column(db.String(100))

    def get_id(self):
        return self.login

# Classe contenant les infos sur les projets

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomProj = db.Column(db.String(100))
    nomMCD = db.Column(db.String(100))
    descProj = db.Column(db.String(500))
    mcd_textuel = db.Column(db.String(500))

# Classe contenant les droits d'un utilisateur sur un projet

class Droit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomDroit = db.Column(db.String(100))
    descDroit = db.Column(db.String(500))

#classe liant Projet, Droit et User

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

# Classe pour stocker les infos des entités d'un mcd d'un projet

class Entite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key = True)
    nomEntite = db.Column(db.String(100))
    positionEntite = db.Column(db.String(100))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetEntite", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{};{}".format(self.id,self.projet_id,self.nomEntite,self.positionEntite)

# Classe pour stocker les infos sur les attributs

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
        return "{};{};{};{};{};{};{}".format(self.id,self.projet_id,self.entite_id,self.nomAttribut,self.genreAttribut,self.typeAttribut,self.primaryKey)

# Classe pour stocker les infos sur les Relations

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    nomRelation = db.Column(db.String(100))
    projet = db.relationship("Projet", foreign_keys=[projet_id], backref=db.backref("projetRelationn", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{}".format(self.id,self.projet_id,self.nomRelation)

# Classe reliant entité et relation

class Relationentite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relation_id = db.Column(db.Integer, db.ForeignKey("relation.id"), primary_key=True)
    relation = db.relationship("Relation", foreign_keys=[relation_id], backref=db.backref("relationid", lazy="dynamic"))
    entite_id = db.Column(db.Integer, db.ForeignKey("entite.id"), primary_key=True)
    cardinaliteE = db.Column(db.String(100))
    entite = db.relationship("Entite", foreign_keys=[entite_id], backref=db.backref("Entite", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{};{}".format(self.id,self.relation_id,self.entite_id,self.cardinaliteE)

# classe stockant les attributs des relations

class Relationattributs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projet.id"), primary_key=True)
    relation_id = db.Column(db.Integer, db.ForeignKey("relation.id"), primary_key=True)
    relation = db.relationship("Relation", foreign_keys=[relation_id], backref=db.backref("relationattid", lazy="dynamic"))
    attribut_id = db.Column(db.Integer, db.ForeignKey("attributs.id"), primary_key=True)
    attributs = db.relationship("Attributs", foreign_keys=[attribut_id], backref=db.backref("attributid", lazy="dynamic"))

    def __repr__(self):
        return "{};{};{};{}".format(self.id,self.relation_id,self.relation,self.attribut_id)

# Permet de récupérer toutes information sur les projets

def get_tout_du_projet(idprojet):
    liste = []
    listeE = Entite.query.filter(Entite.projet_id==idprojet).all()
    listeA = Attributs.query.filter(Attributs.projet_id==idprojet).all()
    print(listeA)
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

# classe pour stocker toutes les informations sur les Notification

class Notification(db.Model):
    nom= db.Column(db.Integer, primary_key=True)
    expediteur=db.Column(db.String(100),db.ForeignKey("user.login"),primary_key=True)
    destinataire=db.Column(db.String(100),db.ForeignKey("user.login"),primary_key=True)
    idProj=db.Column(db.Integer,db.ForeignKey("projet.id"), primary_key=True)
    texte=db.Column(db.String(300))
    date=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

# Permet de trouver le nombre de notifs

def get_nb_notifications(nom):
    return len(Notification.query.filter(Notification.destinataire==nom).all())

# trouve les notification en fonction des du nom de la personne

def get_notifications(nom):
    return Notification.query.filter(Notification.destinataire==nom).order_by(Notification.date.desc()).all()

# trouver les users

def get_user(login):
    User = User.query.filter(User.login==login).all()
    return User

# trouve un projet selon sont id

def get_proj(idProj):
    projet = Projet.query.filter(Projet.id==idProj).all()
    return projet

#  compte le nomnbre total d'entité

def get_nbid_entity():
    allent= Entite.query.all()
    res=[0]
    for a in allent:
        res.append(a.id)
    return max(res)

def get_relationEntite_idEnt(idEntite):
    allrelent = Relationentite.query.filter(Relationentite.entite_id == idEntite).all()
    res=[]
    for a in allrelent:
        res.append(a)
    return res

#  compte le nomnbre total d'attributs

def get_nbid_attribut():
    req = db.session.query(db.func.count(Attributs.id)).scalar()
    return req

# load les user selon leur login

@login_manager.user_loader
def load_user(login):
    return User.query.get(login)

# trouve les logins des users

def get_all_login():
    users=User.query.all()
    res=[]
    for u in users:
        res.append((u.login,u.login))
    return res

# retounr les droits

def get_all_droit():
    droits=Droit.query.all()
    res=[]
    for d in droits:
        res.append((d.id,d.nomDroit))
    return res

# retourne les projets d'un certain user selon sont nom

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

# trouve les projets selon sont id et selon l'utilisateur connecté

def get_projet(username, idProj):
    projets = Projet.query.join(Gerer).filter(Gerer.user_login==username).all()
    for p in projets:
        if p.id == idProj:
            return p
    return None

# trouve le projet selon sont nom

def get_Projet_byName(name):
    return Projet.query.filter(Projet.nomProj==name).first()

# trouve le Gerer selon le nom du projet

def get_gerer_byProjet(nomProj):
    return Gerer.query.join(Projet).filter(Projet.nomProj==nomProj).all()

def get_gerer_byNom(nomProj,nom):
    # print(Gerer.query.join(Projet).filter(Projet.nomProj==nomProj,Gerer.user_login==nom).all())
    return Gerer.query.join(Projet).filter(Projet.nomProj==nomProj,Gerer.user_login==nom).first()
# trouve l'id d'un droit

def get_id_droit(nomDroit):
    return Droit.query.filter(Droit.nomDroit==nomDroit).first().id

# trouve le droit selon sont id

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

#  trouve les attributs de tout un projet

def get_attributs_projet(idProj):
    allatt= Attributs.query.join(Projet).filter(Projet.id==idProj).all()
    res=[]
    for elem in allatt:
        res.append(elem)
    return res


#  trouve un user selon le nom d'un projet

def get_nom_entites_projet(idProj):
    allent= Entite.query.join(Projet).filter(Projet.id==idProj).all()
    res=[]
    for a in allent:
        res.append(a.nomEntite)
    return res

# trouve l'id des entités du projet actuel

def get_id_entites_projet(idProj):
    allent= Entite.query.join(Projet).filter(Projet.id==idProj).all()
    res=[]
    for a in allent:
        res.append(a.id)
    return res

# trouve les entités d'un projet

def get_entites_projet(idProj):
    allent= Entite.query.join(Projet).filter(Projet.id==idProj).all()
    res=[]
    for a in allent:
        res.append(a)
    return res

#  trouve les user d'un projet grâce au nom

def get_user_projet(nomProj):
    gerer=get_gerer_byProjet(nomProj)
    res=[]
    for g in gerer:
        res.append(g.user_login)
    return res

#  trouve les attributs d'un projet selon sont id

def get_attributs_proj(idProj):
    return Attributs.query.filter(Attributs.projet_id == idProj).all()


# trouve les entité grâce au projet actuel

def get_entite_proj(idProj):
    return Entite.query.filter(Entite.projet_id == idProj).all()

# trouve les masters d'un projet
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

# trouve les entités d'un projet selon sont id

def get_entity(idProj):
    return Entite.query.filter(Entite.projet_id == idProj).all()

# trouve une entité d'un projet selon son nom

def get_entitybyname(idProj,nom):
    return Entite.query.filter(Entite.projet_id == idProj,Entite.nomEntite==nom).first()

# trouve les attributs d'un projet selon son nom

def getattributbyname(idProj,nom):
    return Attributs.query.filter(Attributs.projet_id == idProj,Attributs.nomAttribut==nom).first()

# trouve les relations d'un projet grâce à l'id

def getrelations(idProj):
    return Relation.query.filter(Relation.projet_id== idProj).all()
# trouve toutes les classes relationsentites

def getrelationsentites():
    return Relationentite.query.all()

# trouve toutes les classes Relationattributs
def getrelationsattributs(idProj):
    return Relationattributs.query.filter(Relationattributs.projet_id==idProj).all()

# trouve les Relationattributs selon le projet et l'id d'une relation

def get_relAtt_byProjRel(idProj, idRel):
    return Relationattributs.query.filter(Relationattributs.projet_id==idProj).filter(Relationattributs.relation_id==idRel).all()

#  trouve l'entitéRelation selon l'id d'une relation

def get_entityrel_byIdRel(idRel):
    return Relationentite.query.filter(Relationentite.relation_id==idRel).all()
# trouve la premiere relation selon l'id d'une relation et le projet actuel

def get_relation_byId(idRel, idProj):
    return Relation.query.filter(Relation.id == idRel).filter(Relation.projet_id == idProj).one()

# trouve les droits d'un user sur un projet

def getDroitUser(username,idProj):
    return (Gerer.query.filter(Gerer.user_login==username,Gerer.projet_id==idProj).first()).droit.nomDroit

# trouve les relationsAttribut selon l'id d'un attribut et le projet actuel

def get_relAtt_byAtt(attId, idProj):
    return Relationattributs.query.filter(Relationattributs.attribut_id == attId).filter(Relationattributs.projet_id == idProj).all()
