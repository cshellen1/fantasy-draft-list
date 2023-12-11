"""tests for user views"""

import pdb
from unittest import TestCase
from models import db, User, List, connect_db 
from app import app
from flask import session

# configuration changes for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fantasy-list-testdb'
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# connect_db has to be commented out in the app.py before running the test file. So that when the app is initiallized the configuration changes will be read. 
# connect_db(app)

db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    """Test views for user."""
    
    
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        List.query.delete()

        self.client = app.test_client()

        
        testuser = User.register(username="testuser",
                                    email="test@test.com",
                                    first_name="testfirstname",
                                    last_name="testlastname",
                                    password="testpassword")
        
        db.session.add(testuser)
        db.session.commit()
        
        self.testuser = testuser
        
    def test_user_login_page(self):
        """test that the login form is displayed"""
        
        resp = self.client.get("/login")
        html = resp.text
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<button class="btn btn-success">Login</button>', html)
        
        
    def test_user_login(self):
        """test that the user is successfully logged in given valid cradentials"""
        
        d = {'username': self.testuser.username, 
                'password': 'testpassword'}
        
        resp = self.client.post("/login", data=d, follow_redirects=True)
        html = resp.text

        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'Welcome back {self.testuser.first_name}!', html)
        
    def test_loggedout_home_page(self):
        """test that when no user is logged in the home page is displayed with the registration link"""
        
        
        resp = self.client.get('/')
        html = resp.text
            
        self.assertEqual(resp.status_code, 200)
        self.assertIn('href="/register', html)
            
    def test_loggedin_home_page(self):
        """test that when a user is logged in the home page is displayed without the registration link"""
        
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
            
        resp = self.client.get('/')
        html = resp.text
        
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('href="/register', html)
        
        sess.pop('USER_ID')
            
    def test_logout(self):
        """test that a user is successfully logged out and redirected to the home page."""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['USER_ID'] = self.testuser.id
                sess['USERNAME'] = self.testuser.username
                
            resp = self.client.get('/logout')
            
            self.assertEqual(resp.status_code, 302)
            self.assertIsNone(session.get('USERNAME'))
            self.assertIsNone(session.get('USER_ID'))
            
    def test_user_profile(self):
        """test that the user profile is successfully displayed when a user is logged in."""
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
            
        resp = self.client.get(f"/user/{self.testuser.id}/details")
        html = resp.text
        
        self.assertIn(f"{self.testuser.first_name}'s Lists", html)
        self.assertAlmostEqual(resp.status_code, 200) 
            
    def test_user_profile_auth(self):
        """test that you are redirected when trying to access a user profile while not logged in"""

        resp = self.client.get(f"/user/{self.testuser.id}/details")
        html = resp.text
        
        self.assertAlmostEqual(resp.status_code, 302)
        self.assertIn('<a href="/">/</a>', html)
        
    def test_user_registration(self):
        """test that a user is registered successfully and is redirected to the new users profile page"""
        
        d = {"username": "testuser2",
             "first_name": "testfirstname2",
             "last_name": "testlastname2",
             "password": "testpassword2",
             "email": "test2@test.com"}
        
        resp = self.client.post("/register", data=d, follow_redirects=True)
        html = resp.text
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn(f"testfirstname2's Lists", html)
        self.assertIsInstance(User.query.filter_by(username = "testuser2").first(), User)