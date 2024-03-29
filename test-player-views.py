"""tests for player views"""

import os

import pdb
from unittest import TestCase
from models import db, Player, connect_db, User, List, drop_all_tables 
from flask import session, jsonify

# change eviromental variable for testing_database before importing the app
os.environ["DATABASE_URL"] = "postgresql:///fantasy-list-testdb"
# change flask environmental variable so data_check() is not performed in main app and data from api is not added to the test database.
os.environ["FLASK_ENV"] = "testing"

from app import app
# configuration changes for testing

app.config['WTF_CSRF_ENABLED'] = False

drop_all_tables()
db.create_all()

class PlayerViewTestCase(TestCase):
    """Test views for player."""
    
    def setUp(self):
        """create test cleint and add sample data"""

        self.client = app.test_client()
        
        player1 = Player(name="name1",
                        team="team1",
                        points=1000,
                        assists=300,
                        blocks=200,
                        field_goal_percent=0.53,
                        three_percent=0.43,
                        minutes_played=300,
                        season=2023, 
                        games_started=50, 
                        games_played= 45,
                        ftp=0.80, 
                        stl=15, 
                        tov=2, 
                        orb=20,
                        drb=5,
                        trb=25,
                        age=22, 
                        pf=5)
     
        
        player2 = Player(name="name2",
                        team="team2",
                        points=7000,
                        assists=500,
                        blocks=500,
                        field_goal_percent=0.80,
                        three_percent=0.70,
                        minutes_played=500,
                        season=2023, 
                        games_started=50, 
                        games_played= 45,
                        ftp=0.80, 
                        stl=15, 
                        tov=2, 
                        orb=20,
                        drb=5,
                        trb=25,
                        age=22, 
                        pf=5)
        
        player3 = Player(name="name3",
                        team="team3",
                        points=7000,
                        assists=500,
                        blocks=500,
                        field_goal_percent=0.80,
                        three_percent=0.70,
                        minutes_played=500,
                        season=2023, 
                        games_started=50, 
                        games_played= 45,
                        ftp=0.80, 
                        stl=15, 
                        tov=2, 
                        orb=20,
                        drb=5,
                        trb=25,
                        age=22, 
                        pf=5)
        
        player4 = Player(name="name4",
                        team="team4",
                        points=7000,
                        assists=500,
                        blocks=500,
                        field_goal_percent=0.80,
                        three_percent=0.70,
                        minutes_played=500,
                        season=2023, 
                        games_started=50, 
                        games_played= 45,
                        ftp=0.80, 
                        stl=15, 
                        tov=2, 
                        orb=20,
                        drb=5,
                        trb=25,
                        age=22, 
                        pf=5)
        
        player5 = Player(name="name5",
                        team="team5",
                        points=7000,
                        assists=500,
                        blocks=500,
                        field_goal_percent=0.80,
                        three_percent=0.70,
                        minutes_played=500,
                        season=2023, 
                        games_started=50, 
                        games_played= 45,
                        ftp=0.80, 
                        stl=15, 
                        tov=2, 
                        orb=20,
                        drb=5,
                        trb=25,
                        age=22, 
                        pf=5)
        
        testuser = User.register(username="testuser",
                                    email="test@test.com",
                                    first_name="testfirstname",
                                    last_name="testlastname",
                                    password="testpassword")
        
        db.session.add(player1)
        db.session.add(player2)
        db.session.add(player3)
        db.session.add(player4)
        db.session.add(player5)
        db.session.add(testuser)
        db.session.commit()
        
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        self.testuser = testuser
        
    def tearDown(self):
        
        User.query.delete()
        Player.query.delete()
        List.query.delete()
        
    def test_comparison_player_search(self):
        """test that two players data are returned from a comparison search in json form for the dom manipulation in the js file"""
        
        args = {"player1": "name1",
                "player2": "name2"}
        
        resp = self.client.get("/player/search", query_string=args)
        
        # This is a representation of the json in string form that should be returned by the route.
        players_json = '{"player1":{"assists":300,"blocks":200,"field_goal_percent":0.53,"id":1,"minutes_played":300,"name":"name1","points":1000,"team":"team1","three_percent":0.43},"player2":{"assists":500,"blocks":500,"field_goal_percent":0.8,"id":2,"minutes_played":500,"name":"name2","points":7000,"team":"team2","three_percent":0.7}}'
        
        self.assertIn(players_json, resp.text)
        self.assertEqual(resp.status_code, 201)
        
    def test_single_player_search(self):
        """test an individual player search displays the player data when a user is signed in""" 
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
        
        resp = self.client.get('/player/details', query_string={"q": self.player1.name})
        html = resp.text
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'<h5 class="card-title text-center mt-2">{self.player1.name}, {self.player1.age} y.o.<br>', html)
           
    def test_player_search(self):
        """test that when a player search is performed with a misspelled/invalid name that a message is displayed telling the user to check spelling or indicate theres no data for the player"""
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
            
        args = {"q": "not real player"}
        resp = self.client.get('/player/details', query_string=args, follow_redirects=True)
        html = resp.text
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn("No data for player. Check spelling.", html)
        
    def test_player_comparison(self):
        """test that a page is displayed with the player comparison form and form for creating new draft list"""
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
            
        resp = self.client.get('/player/comparison')
        html = resp.text
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('id="compare-player-form"', html)
        self.assertIn('id="list-form"', html)
        
    def test_new_list(self):
        """test that a new list is created after the new list form is filled out and then redirects to the user detail page"""
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
            
        d = {"name": "test_list",
             "point_guard": "name1",
             "strong_guard": "name2",
             "small_forward": "name3",
             "power_forward": "name4",
             "center": "name5"}
        
        resp = self.client.post('/player/comparison', data=d)
        html = resp.text
        
        self.assertEqual(resp.status_code, 302)
        self.assertIn(f'<a href="/user/{self.testuser.id}/details">/user/{self.testuser.id}/details</a>', html)
        self.assertTrue(self.testuser.lists)
        
    def test_delete_draftlist(self):
        """test that a list can be successfully deleted by the current user"""
        
        with self.client.session_transaction() as sess:
            sess['USER_ID'] = self.testuser.id
            
        test_list = List(
            name="test_list",
            pg_id=1,
            sg_id=2,
            sf_id=3,
            pf_id=4,
            c_id=5,
            user_id=self.testuser.id)
        
        db.session.add(test_list)
        db.session.commit() 
        
        resp = self.client.delete(f"/list/{self.testuser.lists[0].id}/delete")
        html = resp.text
    
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(self.testuser.lists)
        self.assertIn(f'<a href="/user/{self.testuser.id}/details">/user/{self.testuser.id}/details</a>', html)
        