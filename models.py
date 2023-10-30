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
    
    __tablename__ = "users"
    
    def __repr__(self):
        u = self
        return f"<{u.first_name} {u.last_name}>"
   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    
    lists = db.relationship("List", backref='user', cascade="all, delete-orphan")
                         
    
    @classmethod
    def register(cls, username, password, first_name, last_name):
        """register user with hashed password and return user"""
    
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        
        return cls( 
                   username=username, 
                   password=hashed_utf8, 
                   first_name=first_name, 
                   last_name=last_name
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
    """
    
    __tablename__ = "lists"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pg = db.Column(db.String(50), nullable=False)
    sg = db.Column(db.String(50), nullable=False) 
    sf = db.Column(db.String(50), nullable=False) 
    pf = db.Column(db.String(50), nullable=False) 
    c = db.Column(db.String(50), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
        
        