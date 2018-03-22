from flask import Flask
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import smtplib
from flask_mail import Mail,Message

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']= "b1715ebf-801a-4188-900c-87cb7a7d493a"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from flask_script import Manager
manager = Manager(app)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "connexion"

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

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../MCDBD.db'))

app.config.update(
DEBUG = True,
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT = 512,
MAIL_USE_SSL = True,
MAIL_USERNAME = 'arthur.fauvin@free.fr',
MAIL_PASSWORD = 'wxcvbn'
)

mail=Mail(app)
db = SQLAlchemy(app)
