from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SelectField, SearchField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """form for registering a user"""
    
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    
class LoginForm(FlaskForm):
    """form for users to login"""
    
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
class ComparePlayerForm(FlaskForm):
    """form to enter players to compare"""
    
    player1 = SelectField("Player 1", validators=[InputRequired()], description="test", id="player1")
    player2 = SelectField("Player 2", validators=[InputRequired()], id="player2")
    
class ListForm(FlaskForm):
    """form for entering and saving a list"""
    
    name = StringField("List Name", validators=[InputRequired()], id="name")
    point_guard = StringField("Point Guard", validators=[InputRequired()], id="pg")
    strong_guard = StringField("Strong Guard", validators=[InputRequired()], id="sg")
    small_forward= StringField("Small Forward", validators=[InputRequired()], id="sf")
    power_forward = StringField("Power Forward", validators=[InputRequired()], id="pf")
    center = StringField("Center", validators=[InputRequired()], id="c")