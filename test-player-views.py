"""tests for player views"""

import pdb
from unittest import TestCase
from models import db, Player, connect_db 
from app import app
from flask import session

# configuration changes for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fantasy-list-testdb'
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# connect_db has to be commented out in the app.py before running the test file. So that when the app is initiallized the configuration changes will be read. 
connect_db(app)

db.drop_all()
db.create_all()

class PlayerViewTestCase(TestCase):
    """Test views for player."""