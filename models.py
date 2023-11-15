"""Models for Fantasy Draft List."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    app.app_context().push()
    return app


class User(db.Model):
    """users model"""

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<{u.first_name} {u.last_name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(75), nullable=False, unique=True)

    lists = db.relationship('List', backref='user', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        return cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

    @classmethod
    def authenticate(cls, username, password):
        """validate user exists and password is correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class List(db.Model):
    """First choice list of players to draft.
    including positions:
    pg = point guard
    sg = shooting guard
    sf = small forward
    pf = power forward
    c = center
    players stored as their id
    """

    __tablename__ = 'lists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pg = db.Column(db.Integer, default='point guard')
    sg = db.Column(db.Integer, default='shooting guard')
    sf = db.Column(db.Integer, default='strong forward')
    pf = db.Column(db.Integer, default='power forward')
    c = db.Column(db.Integer, default='center')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class Player(db.Model):
    """Table for all the players in the"""
    
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    field_goal_percent = db.Column(db.Float(3))
    three_percent = db.Column(db.Float(3))
    minutes_played = db.Column(db.Integer)
        
class PlayerList(db.Model):
    """Player List model"""
    
    __tablename__ = 'player_list'
    
    player_id = db.Column(db.Integer, db.ForeignKey('players.id', ondelete='CASCADE'), primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id', ondelete='CASCADE'), primary_key=True)