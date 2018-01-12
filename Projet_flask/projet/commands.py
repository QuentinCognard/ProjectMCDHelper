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
