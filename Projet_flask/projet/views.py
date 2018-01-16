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

class UserForm(FlaskForm):
	id = HiddenField('id')
	nom = StringField('Nom :')
	prenom = StringField('Prénom :')
	photo = FileField('Photo de profil :')


class CreerCompteForm(FlaskForm):
	login = StringField('Login :')
	nom = StringField('Nom :')
	prenom = StringField('Prenom :')
	password = PasswordField('Mot de passe :')
	confirm_password = PasswordField('Confirmer mot de passe :')
	mail = StringField('Mail :')

@app.route("/") #route pour la page de connexion
def home():
	return render_template("home.html", title= "Exerciseur MCD")

@app.route("/lucas/test/<id_projet>", methods=('GET', 'POST')) #route pour la page de connexion
def lucas(id_projet):
	listeEntite = Entite.query.filter(Entite.projet_id == id_projet).all()
	mon_dictionnaire = {}
	for e in listeEntite:
		mon_dictionnaire[e] = Attributs.query.filter(Attributs.projet_id == id_projet, Attributs.entite_id == e.id).all()
	listeRelation = Relation.query.filter(Relation.projet_id == id_projet).all()
	# listeRelationEntite = []
	# for e in listeEntite:
	# 	listeRelationEntite.append(RelationEntite.query.filter(entite.id == e.id).all())
	# , liste_attribut = listeAttribut,liste_relation = listeRelation,liste_entite_relation = listeRelationEntite
	return render_template("test.html", dic_entite_attribut = mon_dictionnaire, liste_relation = listeRelation)

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

@app.route("/profil/")
@login_required
def accueil_compte():
	user = current_user
	return render_template("profil_user.html", sujet='accueil', user = user)

@app.route("/profil/editer/", methods=('GET', 'POST'))
@login_required
def editer_compte():
	user = current_user
	form = UserForm(nom = user.nom, prenom = user.prenom, photo = user.image)
	return render_template("profil_user.html", sujet='edit', user = user, form = form)

@app.route("/profil/save_edit/", methods=('GET', 'POST'))
@login_required
def save_compte():
	user = current_user
	form = UserForm()
	if form.validate_on_submit():
		if form.nom.data != "":
			user.nom = form.nom.data
		if form.prenom.data != "":
			user.prenom = form.prenom.data
		print(form.photo.data)
		print("####################################")
		if form.photo.data != "":
			f = form.photo.data
			filename = secure_filename(f.filename)
			user.image = filename
			f.save(os.path.join(mkpath('static/images/User/'), filename))
		db.session.commit()
		return redirect(url_for('home'))
	return redirect(url_for('editer_compte'))


@app.route("/logout/")
@login_required
def deconnexion():
	logout_user()
	return redirect(url_for('home'))


@app.route("/creer_compte/",methods=('GET', 'POST'))
def creer_compte():
	f = CreerCompteForm()
	if f.validate_on_submit():
		user = User.query.get_user(f.login.data)
		if user is not None:
			return render_template("creerComptes.html",form = f,error=True)
		else:
			newuser(f.login.data,f.login.password)
			user = User.query.get_user(f.login.data)
			login_user(user)
			return render_template("home.html")
	return render_template("creerComptes.html",form = f,error=False)



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

@app.route("/projets/<string:username>")#accueil avec listes des projets de l'utilsateur et la liste de tous les projets de l'application
def page_projets_parcequelesfonctionsdoiventpasavoirlememenom(username):
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
@login_required
def page_projet_perso():
	return render_template("consult_own_project.html")

# route vers la creation d'un MCD en fonction de l'ID du projet

@app.route("/projets/0/new-mcd")
@login_required
def page_creer_mcd():
	return render_template("create_mcd.html")
