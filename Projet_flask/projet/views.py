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


@app.route("/projets/<string:username>")#accueil avec listes des projets de l'utilsateur et la liste de tous les projets de l'application
def page_projets(username):
	proj=get_projet_user(username)
	return render_template("accueil_projet.html",proj=proj)
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators
from wtforms.validators import DataRequired

class ProjetForm(FlaskForm):#Formulaire de création de projet
	name = StringField('Nom Projet',[validators.Length(min=4, max=25)])
	description =StringField('Description',[validators.Length(min=10, max=150)])
	def createProjet(self,name,description):
		P=Projet(nomProj=name,nomMCD="",descProj=description)
		db.session.add(P)

class DroitProjForm(FlaskForm):
	login=SelectField('Login',choices=get_all_login())
	droit=SelectField('Droit',choices=get_all_droit())

@app.route("/projets/add/<string:username>", methods=['GET', 'POST'])# Page de création d'un projet
def add_projets(username):
	P = ProjetForm(request.form)
	if request.method == 'POST': #Si le formulaire a été rempli
		P.createProjet(P.name.data,P.description.data) #création nouveau projet
		gerer=Gerer(get_Projet_byName(P.name.data).id, username, 1)
		db.session.add(gerer)
		db.session.commit()
		return redirect(url_for("page_projets",username=username))
	return render_template(
		"add-projet.html",
		form=P ,username=username)

@app.route("/projets/<string:username>/<string:nomProj>/parametres")
def parametresProj(username,nomProj):
	return render_template("parametres.html",username=username,nomProj=nomProj)

@app.route("/projets/<string:username>/<string:nomProj>/parametres/Membres")
def membres(username,nomProj):
	membresProj=get_gerer_byProjet(nomProj)
	print(User.query.all())
	return render_template("membres.html",username=username,nomProj=nomProj,membresProj=membresProj)

@app.route("/projets/<string:username>/<string:nomProj>/parametres/Membres/add", methods=['GET', 'POST'])
def add_membre(username,nomProj):
	D=DroitProjForm(request.form)
	if request.method=="POST":
		db.session.add(Gerer(get_Projet_byName(nomProj).id,D.login.data,D.droit.data))
		db.session.commit()
		return redirect(url_for("membres",username=username,nomProj=nomProj))
	return render_template("add-membre.html",username=username,nomProj=nomProj,form=D)
@app.route("/projets/<string:username>/<string:nomProj>/parametres/membres/modif/<string:droit>/<string:nom>",methods=['GET', 'POST'])
def modifier_membres(username,nomProj,droit,nom):
	if( get_nom_droit(get_gerer_byNom(nomProj,nom).droit_id) != "master"):
		idProj=get_Projet_byName(nomProj).id
		db.session.delete(get_gerer_byNom(nomProj,nom))
		db.session.add(Gerer(idProj,nom,get_id_droit(droit)))
		db.session.commit()
	else:
		flash(" impossible : "+nom+" est master")
	return redirect(url_for("membres",username=username,nomProj=nomProj))
@app.route("/projets/<string:username>/<string:nomProj>/parametres/membres/supprimer/<string:nom>", methods=['GET','PÔST'])
def supprimer_membres(username,nomProj,nom):
	if( get_nom_droit(get_gerer_byNom(nomProj,nom).droit_id) != "master"):
		idProj=get_Projet_byName(nomProj).id
		db.session.delete(get_gerer_byNom(nomProj,nom))
		db.session.commit()
		flash(""+nom+" à été supprimer de la liste des membres")
	else:
		flash("impossible : "+nom+" est master")
	return redirect(url_for("membres",username=username,nomProj=nomProj))


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

# route vers la creation d'un MCD en fonction de l'ID du projet

@app.route("/projets/0/new-mcd")
def page_creer_mcd():
	return render_template("create_mcd.html")
