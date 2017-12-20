from .app import app
from .app import db
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired

class ConnexionForm(FlaskForm):
	login = StringField('Login', validators=[DataRequired()])
	password = PasswordField('Mot de passe', validators=[DataRequired()])

@app.route("/")
def home():

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


@app.route("/projets")
def page_projets():
	return render_template("accueil_projet.html")

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

@app.route("/projets/0/new-mcd")
def page_creer_mcd():
	return render_template("create_mcd.html")
