"""Draft List application."""
import requests, random, json
import pdb
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, List, PlayerList, Player
from forms import RegisterForm, LoginForm, ComparePlayerForm, ListForm
from sqlalchemy.sql.functions import ReturnTypeFromArgs
 
class unaccent(ReturnTypeFromArgs):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fantasy-listdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "iliketrucks12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


def run_login(user):
    """Login a user by saving the username and id to the session"""
    
    session["USER_ID"] = user.id
    session["USERNAME"] = user.username
    
def make_dbplayers(players):
    """Create instances of Player to store in the table players"""
    
    for player in players:
        dbplayer = Player(
            name=player['player_name'], 
            team=player['team'],
            points=player['PTS'],
            assists=player['AST'],
            blocks=player['BLK'],
            field_goal_percent=player['field_percent'],
            three_percent=player['three_percent'],
            minutes_played=player['minutes_played'])
        
        db.session.add(dbplayer)
        
        
def add_player_data():
    """Retrieve the API data (player stats) and add all the player stats to local db.
    Need to call this function manually in order to seed the players table."""
    
    r = requests.get(f"https://nba-stats-db.herokuapp.com/api/playerdata/season/2023")
    resp = r.json()
    players = resp['results']
    make_dbplayers(players)
    # resp contains 100 players per response
    while resp['next']:
        r = requests.get(resp['next'])
        resp = r.json()
        players = resp['results']
        make_dbplayers(players)
    
    db.session.commit()
    
    return

def data_check():
    """check to see if there is currently data in the local database and if not add the data"""
    if Player.query.count() == 0:
        add_player_data()
        return

data_check()

def authorization_check():
    """check to see if the user is logged in and """
    
    if  not session["USER_ID"]:
        flash("Restricted access, Please login", "danger")

    else:
        return True
    
####################### general user routes ###########################

@app.route("/")
def show_home():
    """Shows home page"""
    
    return render_template("home.html")

@app.route('/register', methods=["POST", "GET"])
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
        
        run_login(new_user)
        
        return redirect(f"/user-detail/{new_user.id}")
    
    return render_template('register.html', form=form)

@app.route("/user-detail/<int:id>")
def show_user_profile(id):
    """If user logged in shows user profile with all user details."""
    
    if not session.get("USER_ID", None) == None:
        user = User.query.get_or_404(id)
        
        return render_template("user-profile.html", user=user)
        
    else:
        flash("Invalid Credentials", "danger")
        return redirect("/")   
    
@app.route("/logout")
def logout():
    """If user logged in logout user by removing user info from session."""
    
    session.pop("USERNAME")
    session.pop("USER_ID")
    
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """If given valid credentials login user by adding user ingo to session."""
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        
        if user:
            flash(f"Welcome back {user.first_name}!", "success")
            run_login(user)
            
            return redirect(f"/user-detail/{user.id}")
    
        else:
            flash("Invalid Username/Password", "danger")
        
            return redirect("/login")
        
    return render_template("login.html", form=form)

################## player search and comparison routes #########################

@app.route("/player-search")
def get_player_dbdata():
    """get player data from local db and return as JSON"""
    
    p1 = request.args['player1']
    p2 = request.args['player2']
    print(f"##########################request.args: {request.args}")
    player1 = Player.query.filter(unaccent(Player.name).ilike(f"%{p1}%")).first()
    player2 = Player.query.filter(unaccent(Player.name).ilike(f"%{p2}%")).first()
    print(f"##########################player1:{player1}")
    
    response_json = jsonify(player1=player1.serialize(), player2=player2.serialize())
    print(f"########################response: {response_json}")
    return ((response_json, 201))

@app.route("/player-details")
def show_player_search_details():
    """Handle user search for a specific player and display player stats"""
    
    if request.args.get("q"):
    
        player_search = request.args.get("q")
        
        players = Player.query.filter(unaccent(Player.name).ilike(f"%{player_search}%")).all()
        
        if players == []:
            flash("No data for player. Check spelling.", "danger")
            
            return redirect('/player-details')
    
        return render_template("players.html", players=players)
    
    else:
        players = Player.query.filter(Player.id.between(random.randint(1,304), random.randint(305,609))).limit(8).all()
        
        return render_template("players.html", players=players)
        
@app.route("/comparison")
def compare_players():
    """Show page for comparing player statistics and add players to user draft list."""
    
    form1 = ComparePlayerForm()
    form2 = ListForm()
    
    if form2.validate_on_submit():
        pg = db.session.query(Player.id).filter(Player.name.ilike("form2.power_forward.data")).first()
        sg = db.session.query(Player.id).filter(Player.name.ilike("form2.power_forward.data")).first()
        sf = db.session.query(Player.id).filter(Player.name.ilike("form2.power_forward.data")).first()
        pf = db.session.query(Player.id).filter(Player.name.ilike("Jamal Murray")).first()
        c = db.session.query(Player.id).filter(Player.name.ilike("Jamal Murray")).first()
        pg_id = pg.id
        sg_id = sg.id
        sf_id = sf.id
        pf_id = pf.id
        c_id = c.id
        user_id = session["USER_ID"]
        list = List(pg_id=pg_id, sg_id=sg_id, sf_id=sf_id, pf_id=pf_id, c_id=c_id, user_id=user_id)
        
    
    return render_template("compare.html", form1=form1, form2=form2)

####################### list routes ############################

@app.route("/add-players", methods=['POST'])
def add_player_to_draftlist():
    """Add user selcted player to user draftlist"""
    
    
    