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
@login_required
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
@login_required
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

# @app.route("/projets/<idProj>/")
# def page_projet_perso(idProj):
	# proj = get_proj(idProj)
	# if proj:
	# 	return render_template("consult_own_project.html", projet = proj)
	# else:
	# 	return "Projet inconnu"
	# Pour plus tard
@app.route("/projets/0")
@login_required
def page_projet_perso():
	return render_template("consult_own_project.html")

# route vers la creation d'un MCD en fonction de l'ID du projet

@app.route("/projets/0/new-mcd")
@login_required
def page_creer_mcd():
	return render_template("create_mcd.html")
