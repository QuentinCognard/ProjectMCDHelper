# <<<<<<< HEAD
from .app import app
from .app import db
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired

class ConnexionForm(FlaskForm):
	login = StringField('Login', validators=[DataRequired()])
	password = PasswordField('Mot de passe', validators=[DataRequired()])
# =======
from .app import *
from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired
from flask_login import login_user, current_user, login_required, logout_user
from .models import *
from hashlib import sha256

class LoginForm(FlaskForm):
	login = StringField('Login :')
	password = PasswordField('Mot de passe :')
	next = HiddenField()
# >>>>>>> Arthur/master

	def get_authenticated_user(self):
		user = User.query.get(self.login.data)
		if user is None:
			return None
		m = sha256()
		m.update(self.password.data.encode())
		passwd = m.hexdigest()
		return user if passwd == user.password else None


@app.route("/") #route pour la page de connexion
def home():
# <<<<<<< HEAD

	f = ConnexionForm(login="",password="")
	return render_template("connexion.html", title= "Exerciseur MCD", form=f)

@app.route("/traitement", methods=("POST",))
def traitement():
	f = ConnexionForm()
	if f.validate_on_submit():
		User = get_user(f.login.data)
		if User.mdp == f.password:
			return render_template("test.html", title= "Exerciseur MCD",)
		else:
			ferreur = ConnexionForm(login=f.login.data ,password="")
			return render_template("connexion.html", title= "Exerciseur MCD", form=ferreur)
	f = ConnexionForm(login="",password="")
	return render_template("connexion.html", title= "Exerciseur MCD", form=f)

	return render_template("connexion.html", title= "Premier template avec Flask")
# =======
	return render_template("home.html", title= "Exerciseur MCD")

@app.route("/login/", methods=('GET', 'POST'))
def connexion():
	f = LoginForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template("connexion.html",form = f)

@app.route("/logout/")
def deconnexion():
	logout_user()
	return redirect(url_for('home'))

# @app.route("/traitement", methods=("POST",))
# def traitement():
# 	f = ConnexionForm()
# 	if f.validate_on_submit():
# 		User = get_user(f.login.data)
# 		if User.mdp == f.password:
# 			return render_template("test.html", title= "Exerciseur MCD",)
# 		else:
# 			ferreur = ConnexionForm(login=f.login.data ,password="")
# 			return render_template("connexion.html", title= "Exerciseur MCD", form=ferreur)
# 	f = ConnexionForm(login="",password="")
# 	return render_template("connexion.html", title= "Exerciseur MCD", form=f)
#
# 	return render_template("connexion.html", title= "Premier template avec Flask")


@app.route("/projets")#accueil avec listes des projets de l'utilsateur et la liste de tous les projets de l'application
def page_projets():
	return render_template("accueil_projet.html")
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators
from wtforms.validators import DataRequired

class ProjetForm(FlaskForm):#Formulaire de création de projet
	id = HiddenField('id')
	name = StringField('Nom Projet',[validators.Length(min=4, max=25)])
	description =StringField('Description',[validators.Length(min=10, max=150)])

@app.route("/projets/add", methods=['GET', 'POST'])# Page de création d'un projet
def add_projets():
	P = ProjetForm(name="",description="")
	return render_template(
		"add-projet.html",
		form=P)

# route vers un projet perso en fonction de l'ID
# >>>>>>> Arthur/master

# @app.route("/projets/<idProj>/")
# def page_projet_perso(idProj):
	# proj = get_proj(idProj)
	# if proj:
	# 	return render_template("consult_own_project.html", projet = proj)
	# else:
	# 	return "Projet inconnu"
	# Pour plus tard
@app.route("/projets/0")
def page_projet_perso():
	return render_template("consult_own_project.html")

# <<<<<<< HEAD
# @app.route("/projets")
# def page_projets():
# 	return render_template("accueil_projet.html")

# route vers un projet perso en fonction de l'ID

# @app.route("/projets/<idProj>/")
# def page_projet_perso(idProj):
	# proj = get_proj(idProj)
	# if proj:
	# 	return render_template("consult_own_project.html", projet = proj)
	# else:
	# 	return "Projet inconnu"
	# Pour plus tard
# @app.route("/projets/0")
# def page_projet_perso():
# 	return render_template("consult_own_project.html")

# =======
# >>>>>>> Arthur/master
# route vers la creation d'un MCD en fonction de l'ID du projet

@app.route("/projets/0/new-mcd")
def page_creer_mcd():
	return render_template("create_mcd.html")

# route vers l'ajout d'une entité

@app.route("/projets/0/new_entity")
def page_ajouter_entite():
	return render_template("add_entity.html")

# route vers le résumé des relations d'un MCD

@app.route("/projets/0/relation_resume")
def page_resume_relation():
	return render_template("relation_resume.html")

# route vers la Premier etape de la creation d'une relation

@app.route("/projets/0/new_relation1")
def page_ajouter_relation1():
	return render_template("new_relation1.html")

# route vers le resumer d'un MCD

@app.route("/projets/0/mcd_resume")
def page_resume_mcd():
	return render_template("mcd_resume.html")
