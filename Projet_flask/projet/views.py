from .app import *
from flask import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from flask_login import login_user, current_user, login_required, logout_user
from .models import *
from .bibliotheque import *
from hashlib import sha256
from werkzeug.utils import secure_filename
import os
import shutil
from flask_wtf import FlaskForm
from functools import wraps
from flask import g, request, redirect, url_for


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
	login = StringField('Login', [validators.Length(min=4, max=25)])
	nom = StringField('Nom', [validators.Length(min=4, max=25)])
	prenom = StringField('Prenom', [validators.Length(min=4, max=25)])
	password = PasswordField('Mot de passe', [
		validators.DataRequired(),
		validators.EqualTo('confirm_password', message='Mot de passe doivent etre égaux')
	])
	confirm_password = PasswordField('Réécrire le mot de passe')
	mail = StringField('Mail', [validators.Length(min=6, max=35)])

class SearchForm(Form):
	search = StringField('')

@app.route("/") #route pour la page de connexion
def home():
	f = CreerCompteForm()
	f_bis = LoginForm()
	return render_template("home.html", title= "Exerciseur MCD",form_bis=f, form=f_bis)

@app.route("/lucas/test/<id_projet>", methods=('GET', 'POST')) #route pour la page de connexion
def lucas(id_projet):
	ecrire_Entite("test2.txt", id_projet)
	return render_template("test.html", sujet = "test")


@app.route("/projets/<string:username>/<int:idProj>/relations")
def test_lucas():
	ecrire_Entite("test2.txt")
	return render_template("new_relations.html",username=username,id=idProj)



@app.route("/login/", methods=('GET', 'POST'))
def connexion():
	f = LoginForm()
	f_bis = CreerCompteForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("page_projets",username=user.login,n=1,i=1)
			return redirect(next)
	return render_template("home.html", title= "Exerciseur MCD",form_bis=f_bis, form = f)

@app.route("/profil/")
@login_required
def accueil_compte():
	user = current_user
	return render_template("profil_user.html", sujet='accueil', user = user,nbnotif=get_nb_notifications(user.login),notifs=get_notifications(user.login))

@app.route("/profil/editer/", methods=('GET', 'POST'))
@login_required
def editer_compte():
	user = current_user
	form = UserForm(nom = user.nom, prenom = user.prenom, photo = user.image)
	return render_template("profil_user.html", sujet='edit', user = user, form = form,nbnotif=get_nb_notifications(user.login),notifs=get_notifications(user.login))

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
		if form.photo.data != "":
			f = form.photo.data
			filename = secure_filename(f.filename)
			user.image = filename
			f.save(os.path.join(mkpath('static/images/User/'), filename))
		db.session.commit()
		return redirect(url_for('accueil_compte'))
	return redirect(url_for('editer_compte'))


@app.route("/logout/")
@login_required
def deconnexion():
	logout_user()
	return redirect(url_for('home'))


@app.route("/creer_compte/",methods=('GET', 'POST'))
def creer_compte():
	f = CreerCompteForm()
	f_bis = LoginForm()
	if f.validate():
		user = User.query.get(f.login.data)
		if user is not None:
			return render_template("home.html",form_bis = f, form = f_bis, title = "Exerciceur de MCD", error=True)
		else:
			m = sha256()
			m.update(f.password.data.encode())
			passwd = m.hexdigest()
			o = User(prenom = f.prenom.data, nom = f.nom.data, mail = f.mail.data, login = f.login.data, password = passwd)
			db.session.add(o)
			db.session.commit()
			login_user(o)
			flash('Votre compte à bien été créer')
			return redirect(url_for('page_projets',username=o.login,n=1,i=1))
	return render_template("home.html",form_bis = f, form = f_bis, title = "Exerciceur de MCD", error=False)




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


@app.route("/projets/<string:username>/<int:n>/<int:i>",  methods=['GET', 'POST'])#accueil avec listes des projets de l'utilsateur et la liste de tous les projets de l'application
@login_required
def page_projets(username,n,i):
	proj=get_projet_user(username,i)
	projets=get_all_projets(n)
	droiteok=True
	if get_all_projets(n+1)==[]:
		droiteok=False
	droite2ok=True
	if get_projet_user(username,i+1)==[]:
		droite2ok=False
	search = SearchForm(request.form)
	if request.method == 'POST':
		return search_results(search,username)
	return render_template("accueil_projet.html",mesproj=proj,tousproj=projets,form=search,n=n,i=i,droite=droiteok,droite2=droite2ok,search=False,username=username,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))

class ProjetForm(FlaskForm):#Formulaire de création de projet
	name = StringField('Nom Projet',[validators.Length(min=4, max=25)])
	description =StringField('Description',[validators.Length(min=10, max=150)])
	def createProjet(self,name,description):
			P=Projet(nomProj=name,nomMCD="",descProj=description)
			db.session.add(P)

class DroitProjForm(FlaskForm):#formulaire pour avoir 2 liste déroulantes avec les users et les droits
	login=SelectField('Login',choices=[])
	droit=SelectField('Droit',choices=[])


@app.route("/projets/add/<string:username>", methods=['GET', 'POST'])# Page de création d'un projet
@login_required
def add_projets(username):
	P = ProjetForm(request.form)
	if request.method == 'POST': #Si le formulaire a été rempli
		if P.validate_on_submit():
			if get_Projet_byName(P.name.data)==None:
				P.createProjet(P.name.data,P.description.data) #création nouveau projet
				gerer=Gerer(get_Projet_byName(P.name.data).id, username, 1)
				db.session.add(gerer)
				db.session.commit()
			else:
				max_sup = 1
				for projet in test("TestProjet"):
					if len(projet.nomProj.split("(")) > 1:
						if max_sup <= int(projet.nomProj.split("(")[1].split(")")[0]):
							max_sup = int(projet.nomProj.split("(")[1].split(")")[0]) + 1
				if max_sup == 1:
					P.createProjet(P.name.data + "(1)",P.description.data) #création nouveau projet
					gerer=Gerer(get_Projet_byName(P.name.data+"(1)").id, username, 1)
				else:
					P.createProjet(P.name.data + "(" + str(max_sup) + ")",P.description.data) #création nouveau projet
					gerer=Gerer(get_Projet_byName(P.name.data + "(" + str(max_sup) + ")").id, username, 1)
				db.session.add(gerer)
				db.session.commit()
			return redirect(url_for("page_projets",username=username,n=1,i=1))
		return render_template(
			"add-projet.html",
			form=P ,username=username,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))
	return render_template(
		"add-projet.html",
		form=P ,username=username,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))
@app.route("/projets/<string:username>/<string:nomProj>/description")
@login_required
def description(username,nomProj):
	membres=get_gerer_byProjet(get_Projet_byName(nomProj).nomProj)
	return render_template("description-projet.html",projet=get_Projet_byName(nomProj),membres=membres,nbnotif=get_nb_notifications(username),master=get_master_proj(nomProj),notifs=get_notifications(username),m=get_gerer_byNom(nomProj,username))

@app.route("/projets/<string:username>/<string:nomProj>/description/<string:master>/notif")
@login_required
def demande(username,nomProj,master):
	if get_notif_byexp_dest_nom("Demande de "+username,username,master,get_Projet_byName(nomProj).id)!=[]:
		flash("Demande déjà envoyé")
	else:
		N=Notification(nom="Demande de "+username,
		expediteur=username,destinataire=master,idProj=get_Projet_byName(nomProj).id,
		texte="Demande de participation à votre projet "+nomProj+" de "+username+". Il sera ajouté en visiteur.")
		db.session.add(N)
		db.session.commit()
		flash("Demande envoyée")
	return redirect("projets/"+username+"/1/1")
@app.route("/projets/<string:username>/<string:user>/<int:id>/<string:reponse>")
def reponsedemande(username,id,reponse,user):
	if reponse=="y":
		db.session.add(Gerer(id,username,3))
		db.session.commit()
		flash(username+" a bien été ajouté au projet")
	db.session.delete(get_notif_byexp_dest_id(username,user,id))
	db.session.commit()
	return redirect("/projets/"+user+"/1/1")


@app.route("/projets/<string:username>/<string:nomProj>/parametres")
@login_required
def parametresProj(username,nomProj):
	gerer=get_gerer_byNom(nomProj,username)
	return render_template("parametres.html",username=username,nomProj=nomProj,gerer=gerer,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))

@app.route("/projets/<string:username>/<string:nomProj>/parametres/suppProj")
def suppProj(username,nomProj):
	if( get_nom_droit(get_gerer_byNom(nomProj,username).droit_id) == "master"):
		gere=get_gerer_byProjet(nomProj)
		if gere !=[] :
			for g in gere:
				db.session.delete(g)
		if get_Projet_byName(nomProj)!=[] :
			db.session.delete(get_Projet_byName(nomProj))
		db.session.commit()
		flash("Le projet "+nomProj+" a bien été supprimé")
	return redirect("/projets/"+username+"/1/1")

@app.route("/projets/<string:username>/<string:nomProj>/parametres/Membres")
@login_required
def membres(username,nomProj):
	membresProj=get_gerer_byProjet(nomProj)
	if( get_nom_droit(get_gerer_byNom(nomProj,username).droit_id) == "master"):
		return render_template("membres.html",username=username,nomProj=nomProj,membresProj=membresProj,master=True,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))
	else:
		return render_template("membres.html",username=username,nomProj=nomProj,membresProj=membresProj,master=False,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))

@app.route("/projets/<string:username>/<string:nomProj>/parametres/Membres/add", methods=['GET', 'POST'])
@login_required
def add_membre(username,nomProj):
	D=DroitProjForm(request.form)
	D.login.choices=get_all_login()
	membresProj=get_user_projet(nomProj)
	supp=[]
	for c in D.login.choices:
		if c[0] in membresProj:
			supp.append(c)
	for elem in supp:
		D.login.choices.remove(elem)
	D.droit.choices=get_all_droit()
	D.droit.choices.remove((1,"master"))
	if request.method=="POST":
		db.session.add(Gerer(get_Projet_byName(nomProj).id,D.login.data,D.droit.data))
		db.session.commit()
		return redirect(url_for("membres",username=username,nomProj=nomProj))
	return render_template("add-membre.html",username=username,nomProj=nomProj,form=D,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))


@app.route("/projets/<string:username>/<string:nomProj>/parametres/membres/modif/<string:droit>/<string:nom>",methods=['GET', 'POST'])
@login_required
def modifier_membres(username,nomProj,droit,nom):
	if( get_nom_droit(get_gerer_byNom(nomProj,nom).droit_id) != "master"):
		idProj=get_Projet_byName(nomProj).id
		db.session.delete(get_gerer_byNom(nomProj,nom))
		db.session.add(Gerer(idProj,nom,get_id_droit(droit)))
		db.session.commit()
	else:
		flash(" impossible : "+nom+" est master")
	return redirect(url_for("membres",username=username,nomProj=nomProj))

@app.route("/projets/<string:username>/<string:nomProj>/parametres/membres/supprimer/<string:nom>", methods=['GET','POST'])
@login_required
def supprimer_membres(username,nomProj,nom):
	if( get_nom_droit(get_gerer_byNom(nomProj,nom).droit_id) != "master"):
		idProj=get_Projet_byName(nomProj).id
		db.session.delete(get_gerer_byNom(nomProj,nom))
		db.session.commit()
		flash(""+nom+" a été supprimé de la liste des membres")
	else:
		flash("impossible : "+nom+" est master")
	return redirect(url_for("membres",username=username,nomProj=nomProj))


@app.route('/projets/<string:username>/results')
@login_required
def search_results(search,username):
	results = []
	search_string = search.data['search']
	proj=get_projet_user(username,1)
	projets=[]
	if search.data['search']== '' or search.data['search']==" ":
		return redirect('/projets/'+username+'/1/1')
	else:
		projets=Projet.query.filter(Projet.nomProj.like("%{}%".format(search_string))).all()
	if projets==[]:
		flash('Pas de résultats')
		return redirect('/projets/'+username+'/1/1')
	else:
		return render_template("accueil_projet.html",mesproj=proj,tousproj=projets,form=SearchForm(request.form),n=1,i=1,droite=False,droite2=True,search=True,username=username,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))

@app.route("/projets/<string:username>/<string:nomProj>/parametres/modifProj")
@login_required
def modifProj(username,nomProj):
	P = ProjetForm(name=nomProj,description=get_Projet_byName(nomProj).descProj)
	return render_template('modifProj.html',form=P,username=username,nomProj=nomProj,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))

@app.route("/projets/<string:username>/<string:nomProj>/parametres/modifProj/save",methods=['GET', 'POST'])
@login_required
def save_modifProj(username,nomProj):
	P = ProjetForm()
	affiche=P.name.data
	projetCourant=get_Projet_byName(nomProj)
	if projetCourant.nomProj==P.name.data:
		flash("le nom n'a pas changé")
	else:
		if P.validate_on_submit():
				if P.name.data != "":
					if get_Projet_byName(P.name.data)==None:
						projetCourant.nomProj = P.name.data
					else:
							max_sup = 1
							for projet in test("TestProjet"):
								if len(projet.nomProj.split("(")) > 1:
									if max_sup <= int(projet.nomProj.split("(")[1].split(")")[0]):
										max_sup = int(projet.nomProj.split("(")[1].split(")")[0]) + 1
							if max_sup == 1:
								projetCourant.nomProj=P.name.data + "(1)"
								affiche=P.name.data + "(1)"
							else:
								projetCourant.nomProj=P.name.data + "(" + str(max_sup) + ")"
								affiche=P.name.data + "(" + str(max_sup) + ")"
				if P.description.data != "":
					projetCourant.descProj = P.description.data
				db.session.commit()
				return redirect(url_for('parametresProj',username=username,nomProj=affiche))
				flash("Le projet à bien été modifié")


		flash("Impossible de modifié le projet, le nom ou la description est trop court(e) ou trop long")
	return redirect(url_for('modifProj',username=username,nomProj=nomProj))

@app.route("/projets/<string:username>/<string:nomProj>/quitter")
@login_required
def quitter(username,nomProj):
	proj=get_projet_user(username,1)
	projets=get_all_projets(1)
	if( get_nom_droit(get_gerer_byNom(nomProj,username).droit_id) != "master"):
		idProj=get_Projet_byName(nomProj).id
		db.session.delete(get_gerer_byNom(nomProj,username))
		db.session.commit()
		flash(""+nomProj+" a été supprimé de la liste de vos projets")
	else:
		flash("impossible de quitter le projet, vous êtes master")
		return redirect('/projets/'+username+'/1/1')
# @app.route("/projets/<idProj>/")
# def page_projet_perso(idProj):
	# proj = get_proj(idProj)
	# if proj:
	# 	return render_template("consult_own_project.html", projet = proj)
	# else:
	# 	return "Projet inconnu"
	# Pour plus tard
@app.route("/projets/<string:username>/<int:idProj>")
@login_required
def page_projet_perso(username, idProj):
	proj = get_projet(username, idProj)
	if proj != None:
		return render_template("consult_own_project.html", projet = proj,username=username,id=idProj,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))
	return redirect(url_for('page_projets', username=username, n=1, i=1))

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


@app.route("/projets/<string:username>/<int:idProj>/new-attributs")
@login_required
def page_new_attributs(username, idProj):
	proj = get_projet(username, idProj)
	print(proj)
	if proj != None:
		return render_template("new_attributs.html", projet = proj,username=username,id=idProj,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))
	return redirect(url_for('page_projets', username=username, n=1, i=1))

@app.route("/projets/<string:username>/<int:idProj>/new-attributs/save/", methods=['POST',])
def save_new_attributs(username, idProj):
	oldAtts = get_attributs_proj(idProj)
	for a in oldAtts:
		db.session.delete(a)
	nbAtt = request.form.get("nbAtt")
	proj = get_projet(username, idProj)
	proj.nomMCD = request.form.get("nomMCD")
	for i in range(1, int(nbAtt)+1):
		att = Attributs(id=i, projet_id=idProj, nomAttribut=request.form.get("nom"+str(i)), genreAttribut=request.form.get("genre"+str(i)), typeAttribut=request.form.get("type"+str(i)))
		db.session.add(att)
	db.session.commit()
	##############
    # A MODIFIER #
	##############
    # DOIT PASSER A LA PAGE DE CREATION D'ENTITES
	return redirect(url_for('page_projet_perso', username=username, idProj=idProj))

@app.route("/projets/<string:username>/<int:idProj>/attributs")
def page_modif_attributs(username, idProj):
	atts = get_attributs_proj(idProj)
	return render_template(
		"modif_attributs.html",
		username=username,
		idProj=idProj,
		attributs=atts,
		nbAtts=len(atts),
		projet=get_projet(username, idProj),nbnotif=get_nb_notifications(username),notifs=get_notifications(username))


@app.route("/projets/<string:username>/<int:idProj>/relations")
@login_required
def page_creer_relations(username, idProj):
	return render_template("new_relations.html",username=username,id=idProj,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))

class CreaMCDForm(FlaskForm):#Formulaire de création d'un MCD
	listeAttribut=SelectField('Attributs',choices=[])

	def addEntite(self,nomEntite,idEntite):
		E=Entite(nomEntite=nomEntite)
		db.session.add(E)

	def moveAttribut(self,idEntite,idAttribut):
		A=Attributs.query.filter_by(id=idAttribut)
		A.entite_id=idEntite
		db.session.commit()

@app.route("/projets/0/new-mcd")
@login_required
def page_creer_mcd():
	return render_template("create_mcd.html")

# route vers l'ajout d'une entité

@app.route("/projets/<string:username>/<int:idProj>/new_entity")
def page_ajouter_entite(username,idProj):
	M=CreaMCDForm(request.form)
	M.listeAttribut.choices = get_attributs_projet(idProj)
	proj = get_proj(idProj)
	if proj != None:
		return render_template("add_entity.html", projet = proj,username=username,id=idProj,attributs=M.listeAttribut.choices, form=M,nbnotif=get_nb_notifications(username),notifs=get_notifications(username))
	return redirect(url_for('page_projets', username=username, n=1, i=1))


@app.route("/projets/<string:username>/<int:idProj>/new_entity/save", methods=['GET', 'POST'])
def save_entity(username,idProj):
	nbAtt = request.form.get("nbAtt")
	nbEnt = request.form.get("nbEnt")
	proj = get_proj(idProj)
	for i in range(1, int(nbEnt)+1):
		if request.method=="POST":
			ent = Entite(id=i, projet_id=idProj, nomEntite=request.form.get("nom"+str(i-1)), positionEntite=i)
			db.session.add(ent)
			db.session.commit()
	for y in range(1, int(nbAtt)+1):
		if request.method=="POST":
			 att = Attributs.query.get(request.form.get("idAtt"))
			 att.entite_id = request.form()
			 get("nbEnt")
			 db.session.commit()
	return render_template("relation_resume.html",username=username,idProj=idProj)

# @app.route("/projets/<string:username>/<int:idProj>/new_entity/save", methods=['GET', 'POST'])
# def save_entity(username,idProj):
# 	nbAtt = request.form.get("nbAtt")
# 	nbEnt = request.form.get("nbEnt")
# 	proj = get_proj(idProj)
# 	for i in range(1, int(nbEnt)+1):
# 		if request.method=="POST":
# 			ent = Entite(id=i, projet_id=idProj, nomEntite=request.form.get("nom"+str(i-1)), positionEntite=i)
# 			db.session.add(ent)
# 			db.session.commit()
# 	for y in range(1, int(nbAtt)+1):
# 		if request.method=="POST":
# 			 att = Attributs.query.get(request.form.get("idAtt"))
# 			 att.entite_id = request.form.()
# 			 get("nbEnt")
# 			 db.session.commit()
# 	return render_template("relation_resume.html")


# route vers le résumé des relations d'un MCD

@app.route("/projets/<string:username>/<int:idProj>/relation_resume")
def page_resume_relation(username,idProj):
	return render_template("relation_resume.html",username=username,idProj=idProj)

# route vers la Premier etape de la creation d'une relation

@app.route("/projets/<string:username>/<int:idProj>/new_relation1")
def page_ajouter_relation1(username,idProj):
	return render_template("new_relation1.html",username=username,idProj=idProj)

# route vers le resumer d'un MCD

@app.route("/projets/<string:username>/<int:idProj>/mcd_resume")
def page_resume_mcd(username,idProj):
	return render_template("mcd_resume.html",username=username,idProj=idProj)
