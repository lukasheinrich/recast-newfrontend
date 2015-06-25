import json
import requests
import importlib

import asynctasks
import synctasks


from flask import Flask, redirect, jsonify, session, request, url_for, render_template, flash
from flask.ext import login as login
from frontendconfig import config as frontendconf
from recastdb.database import db
import recastdb.models as dbmodels
import forms


celeryapp  = importlib.import_module(frontendconf['CELERYAPP']).app

ORCID_APPID = frontendconf['ORCID_APPID']
ORCID_REDIRECT_URI = frontendconf['ORCID_REDIRECT_URI']
ORCID_SECRET = frontendconf['ORCID_SECRET']


class User(login.UserMixin):
  def __init__(self,**kwargs):
    self.orcid = kwargs.get('orcid','no-orcid')
    self.fullname = kwargs.get('fullname','no-name')
  def get_id(self):
    return self.orcid
  def name(self):
    return self.fullname

def create_app():
  app = Flask(__name__)
  app.config.from_object(frontendconf['FLASKCONFIG'])
  db.init_app(app)
  return app
  
app = create_app()

login_manager = login.LoginManager()
login_manager.init_app(app)

@app.route("/")
def home():
  all_users = dbmodels.User.query.all()
  celeryapp.set_current()
  asynctasks.hello_world.delay()
  return render_template('home.html', user_data = all_users)

@app.route("/about")
def about():
  return render_template('about.html')


@app.route('/login')
def login_user():
  if not request.args.has_key('code'):
    return  redirect('https://orcid.org/oauth/authorize?client_id={}&response_type=code&scope=/authenticate&redirect_uri={}&show_login=true'.format(
    ORCID_APPID,
    ORCID_REDIRECT_URI
  ))
  
  auth_code = request.args.get('code')
  data = {'client_id':ORCID_APPID,'client_secret':ORCID_SECRET,'grant_type':'authorization_code','code':auth_code}

  r = requests.post('https://pub.orcid.org/oauth/token', data = data)
  login_details = json.loads(r.content)

  user = User(orcid = login_details['orcid'], fullname = login_details['name'], authenticated = True)
  login.login_user(user)
  
  return redirect(url_for('home'))

@app.route("/form", methods=('GET', 'POST'))
def form():
  myform = forms.AnalysisSubmitForm()
  if myform.validate_on_submit():
    synctasks.createAnalysisFromForm(app,myform,login.current_user)
    flash('success! form validated and was processed','success')
  elif myform.is_submitted():
    flash('failure! form did not validate and was not processed','danger')

  return render_template('form.html', form = myform)
    
@app.route("/logout")
@login.login_required
def logout():
    login.logout_user()
    return redirect('/')  

@login_manager.user_loader
def load_user(userid):
    r = requests.get('http://pub.orcid.org/v1.2/{}/orcid-profile'.format(userid), headers = {'Accept':'application/json'})
    login_bio = json.loads(r.content)['orcid-profile']['orcid-bio']
    return User(orcid = userid, fullname = '{} {}'.format(login_bio['personal-details']['given-names']['value'],login_bio['personal-details']['family-name']['value']))

@login_manager.unauthorized_handler
def unauthorized():
  return redirect(url_for('login_user'))

@app.route("/profile")
@login.login_required
def profile():
  user_query = dbmodels.User.query.filter(dbmodels.User.name == login.current_user.name()).all()
  assert len(user_query)
  return render_template('profile.html', db_user = user_query[0])

@app.route("/analyses")
def analyses():
  analyses = dbmodels.Analysis.query.all()
  tuples = [(dbmodels.User.query.filter(dbmodels.User.id == a.owner_id)[0],a) for a in analyses]
  return render_template('analyses.html', analyses = tuples)

