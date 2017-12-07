from .app import app
from .app import db
from flask import render_template


@app.route("/")
def home():
	return render_template("connexion.html", title= "Premier template avec Flask")


@app.route("/projets")
def page_projets():
	return render_template("accueil_projet.html")
