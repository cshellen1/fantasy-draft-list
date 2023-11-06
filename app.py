"""Draft List application."""

import pdb
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, List
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fantasy-draft-listdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "iliketrucks12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)



# @app.before_request
# def add_user_to_g():
#     """If user logged in, add curr user to Flask global."""

#     if CURR_USER in session:
#         g.user = User.query.get(session[CURR_USER])

#     else:
        # g.user = None

@app.route("/")
def show_home():
    """Shows home page"""
    
    return render_template("home.html")

@app.route('/users/register', methods=["POST", "GET"])
def register_new_user():
    """Show registration form and handle creating new user instance and store in database"""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        email = form.email.data
        
        new_user = User.register(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                        email=email)
        
        db.session.add(new_user)
        db.session.commit()
        
        session["USER_ID"] = new_user.id
        session["USERNAME"] = new_user.username
        
        return redirect(f"/users/{new_user.id}")
    
    return render_template('register.html', form=form)

@app.route("/users/detail/<int:id>")
def show_user_profile(id):
    """If user logged in shows user profile with all user details."""
    
    if session["CURR_USER"]:
        user = User.query.get_or_404(id)
        
        return render_template("user-profile.html", user=user)
        
    else:
        return redirect("/")   
    
@app.route("/users/logout")
def logout():
    """If user logged in logout user by removing user info from session."""
    
    session.pop("USERNAME")
    session.pop("USER_ID")
    session.pop("CURR_USER")
    
    return redirect("/")

# @app.route("/users/login")
# def login():
#     """If given valid credentials login user by adding user ingo to session."""
    
    
    