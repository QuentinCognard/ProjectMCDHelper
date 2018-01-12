from flask import Flask

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']= "b1715ebf-801a-4188-900c-87cb7a7d493a"


from flask_script import Manager
manager = Manager(app)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

import os.path

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('MCDBD.db'))
db = SQLAlchemy(app)
