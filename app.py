"""Draft List application."""
import requests, random, datetime
import pdb, os
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, List, PlayerList, Player
from forms import RegisterForm, LoginForm, ComparePlayerForm, ListForm
from sqlalchemy.sql.functions import ReturnTypeFromArgs
 
class unaccent(ReturnTypeFromArgs):
    pass

app = Flask(__name__)
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///fantasy-listdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
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
            minutes_played=player['minutes_played'],
            season=player['season'],
            games_started=player['games_started'],
            games_played=player['games'],
            ftp=player['ft_percent'],
            stl=player['STL'],
            tov=player['TOV'],
            orb=player['ORB'],
            drb=player['DRB'],
            trb=player['TRB'],
            age=player['age'],
            pf=player['PF'])
        
        db.session.add(dbplayer)

curr_date = datetime.date.today()

def delete_old_player_data():
    """deletes previous years data"""
    
    db.session.query(Player).filter(Player.season == curr_date.year - 1).delete()
    db.session.query(List).delete()
    db.session.query(PlayerList).delete()

    return
        
def update_player_data():
    """Retrieve the API data (player stats) and add all the player stats to local db.
    Need to call this function manually in order to seed the players table."""
    
    r = requests.get(f"https://nba-stats-db.herokuapp.com/api/playerdata/season/{curr_date.year}")
    resp = r.json()
    players = resp['results']
    
    # this checks to make sure the api returned the player data in the response
    if len(players) == 0:
        return
      
    else:
        make_dbplayers(players)
        # resp contains 100 players per response
        while resp['next']:
            r = requests.get(resp['next'])
            resp = r.json()
            players = resp['results']
            make_dbplayers(players)

        delete_old_player_data()
        
        db.session.commit()
    
        return


def data_check():
    """checks to see if there is currently data from the last season in the local database and if not add the data from the most recent previous season ans delete the data from the oldest season in the local database"""
    
    if Player.query.count() == 0:
        update_player_data()
        return
    
    elif curr_date.year > db.session.query(Player.season).first()[0]:
        update_player_data()
        return
   

if not os.environ["FLASK_ENV"] == "testing":
    print("**********Data check performed***********")
    data_check()


def authorization_check():
    """check to see if the user is logged in by looking for the USER_ID in the session"""
    
    if not session.get("USER_ID", None) == None:
    
        return True
    
def get_random(num_records, model):
    """function to get random records of a specified amount"""
    
    existing_ids = [model.id for model in model.query.with_entities(model.id).all()]
    random_indices = random.sample(existing_ids, min(num_records, len(existing_ids)))
    random_records = model.query.filter(model.id.in_(random_indices)).all()
    
    return random_records

####################### general user routes ###########################

@app.route("/")
def show_home():
    """Shows home page"""
    
    lists = get_random(8, List)
    
    return render_template("home.html", lists=lists)

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
        
        return redirect(f"/user/{new_user.id}/details")
    
    return render_template('register.html', form=form)

@app.route("/user/<int:id>/details")
def show_user_profile(id):
    """If user logged in shows user profile with all user details."""
    
    if authorization_check():    
        
        user = User.query.get_or_404(id)
        lists = user.lists
        
        return render_template("user-profile.html", user=user, lists=lists)
        
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
            
            return redirect(f"/user/{user.id}/details")
    
        else:
            flash("Invalid Username/Password", "danger")
        
            return redirect("/login")
        
    return render_template("login.html", form=form)

################## player search and comparison routes #########################

@app.route("/player/search")
def get_player_dbdata():
    """get player data from local db and return as JSON"""
    
    p1 = request.args['player1']
    p2 = request.args['player2']
    
    
    player1 = Player.query.filter_by(name = p1).first()
    player2 = Player.query.filter_by(name = p2).first()
    
    response_json = jsonify(player1=player1.serialize(), player2=player2.serialize())
   
    return ((response_json, 201))

@app.route("/player/details")
def show_player_search_details():
    """Handle user search for a specific player and display player stats"""
    
    if not authorization_check():
        flash("restricted access please login", "danger")
        
        return redirect('/login')
    
    if request.args.get("q"):
    
        player_search = request.args.get("q")
        
        players = Player.query.filter(unaccent(Player.name).ilike(f"%{player_search}%")).all()
        
        if players == []:
            flash("No data for player. Check spelling.", "danger")
            
            return redirect('/player/details')
    
        return render_template("players.html", players=players)
    else:
        
        players = get_random(12, Player)
        
        return render_template("players.html", players=players)
        
@app.route("/player/comparison", methods=["POST", "GET"])
def compare_players():
    """Show page for comparing player statistics and add players to user draft list."""
    
    if not authorization_check():
        flash("restricted access please login", "danger")
        
        return redirect('/login')
    
    all_players_names = Player.query.order_by(Player.name)
    
    form_choices = sorted(set([player.name for player in all_players_names]))
        
    
    form1 = ComparePlayerForm()
    form2 = ListForm()
    form1.player1.choices = form_choices
    form1.player2.choices = form_choices
        
    if form2.validate_on_submit():
        
        pg = db.session.query(Player.id).filter(Player.name.ilike(f"{form2.point_guard.data}")).first()
        sg = db.session.query(Player.id).filter(Player.name.ilike(f"{form2.strong_guard.data}")).first()
        sf = db.session.query(Player.id).filter(Player.name.ilike(f"{form2.small_forward.data}")).first()
        pf = db.session.query(Player.id).filter(Player.name.ilike(f"{form2.power_forward.data}")).first()
        c = db.session.query(Player.id).filter(Player.name.ilike(f"{form2.center.data}")).first()

        name = form2.name.data
        pg_id = pg[0]
        sg_id = sg[0]
        sf_id = sf[0]
        pf_id = pf[0]
        c_id = c[0]
        user_id = session["USER_ID"]
        
        if len(set([pg_id,sg_id,sf_id,pf_id,c_id])) < 5:
            flash('Please select 5 different players', 'danger')
            
            return redirect("/player/comparison")
        
        else:
            
            list = List(name=name, pg_id=pg_id, sg_id=sg_id, sf_id=sf_id, pf_id=pf_id, c_id=c_id, user_id=user_id)
        
            db.session.add(list)
            db.session.commit()
        
            list.add_to_playerlists()
        
        
            return redirect(f"/user/{user_id}/details")
        
    return render_template("compare.html", form1=form1, form2=form2)

####################### list routes ############################

@app.route("/list/<int:id>/delete", methods=["DELETE"])
def delete_draftlist(id):
    """Delete player list"""
    
    if authorization_check():
    
        List.query.filter_by(id=id).delete()
        db.session.commit()
    
        return redirect(f'/user/{session["USER_ID"]}/details')
    
    else:
        flash("Unauthorized please", "danger")
        
        return redirect("/login")
    
    
    
    
    
    