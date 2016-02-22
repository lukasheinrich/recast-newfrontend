import os

import unittest
from recastfrontend.server import create_app
from recastfrontend.server import db
import recastdb.models
from flask import url_for

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        db.session.remove()
        #db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        #response = self.client.get(url_for('./'))
        #self.assetTrue('Stranger' in response.get_data(as_text=True))
        #print self.client.get(url_for('about'))
        #pass
        pass

    def testUser(self):
        user = recastdb.models.User(name="Test User", email="test@email.com")
        db.session.add(user)
        db.session.commit()

    def testAnalysis(self):
        run_condition = recastdb.models.RunCondition(name="run condition test", description="test")
        db.session.add(run_condition)
        db.session.commit()
        analysis = recastdb.models.Analysis(title="Analysis title test", description="Testing description test", collaboration="ATLAS", run_condition_id=run_condition.id, owner_id=1)
        db.session.add(analysis)
        db.session.commit()

    def testRequest(self):
        pass
        

    def testDB(self):
        db.session.query(recastdb.models.User).all()
        
                                    
        
    def getClient(self):
        return self.client
