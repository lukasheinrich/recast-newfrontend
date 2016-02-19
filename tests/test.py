import os

import unittest
from recastfrontend.server import create_app
from recastfrontend.server import db
#from recastfrontend.server import recastdb.models
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
        pass

    def test_home_page(self):
        #response = self.client.get(url_for('./'))
        #self.assetTrue('Stranger' in response.get_data(as_text=True))
        pass

    def testDB(self):
        db.session.query(recastdb.models.User).all()
