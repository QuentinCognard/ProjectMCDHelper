from .app import app, manager,db
import projet.views
import projet.commands
import projet.models
import projet.bibliotheque

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('connexion'))
    return wrap
