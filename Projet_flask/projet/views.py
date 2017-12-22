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
