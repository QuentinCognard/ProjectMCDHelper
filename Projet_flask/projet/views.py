from .app import app
from .app import db
from flask import render_template


@app.route("/")
def home():
	return render_template("connexion.html", title= "Exerciseur MCD")
