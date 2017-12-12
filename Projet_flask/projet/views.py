from .app import app
from .app import db
from flask import render_template


@app.route("/")
def home():
	return render_template("connexion.html", title= "Exerciseur MCD")

@app.route("/test")

def connexion():
	return render_template("connexion.html", title= "Bug", User=get_user(3,"admin"))
