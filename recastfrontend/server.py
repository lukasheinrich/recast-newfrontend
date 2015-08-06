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

# Forms --------------------------------------------------------------------------------

@app.route("/form", methods=('GET', 'POST'))
@login.login_required
def form():
  myform = forms.AnalysisSubmitForm()
  
  run_conditions = dbmodels.RunCondition.query.all()
  
  myform.run_condition_choice.choices = [(str(rc.id),rc.title) for rc in run_conditions]

  if myform.validate_on_submit():
    synctasks.createAnalysisFromForm(app,myform,login.current_user)
    flash('success! form validated and was processed','success')
  elif myform.is_submitted():
    print myform.errors
    flash('failure! form did not validate and was not processed','danger')

  return render_template('form.html', form = myform)


@app.route("/userform", methods=('GET', 'POST'))
def user_form():
  userform = forms.UserSubmitForm()

  if userform.validate_on_submit():
    synctasks.createUserFromForm(app,userform)
    flash('success! form validated and was processed', 'success')
  elif userform.is_submitted():
    print userform.errors
    flash('failure! form did not validate and was not processed', 'danger')
    
  return render_template('form.html', form=userform)


@app.route("/modelform", methods=('POST', 'GET'))
@login.login_required
def model_form():
  model_form = forms.ModelSubmitForm()

  if model_form.validate_on_submit():
    synctasks.createModelFromForm(app,model_form,login.current_user)
    flash('success! Model form validated and was processed', 'success')
    
  elif model_form.is_submitted():
    print model_form.errors
    flash('failure! Model form did not validate and was not processed', 'danger')
    
  return render_template('form.html', form=model_form)
             
@app.route("/runform", methods=('GET', 'POST'))
@login.login_required
def run_condition_form():
  run_condition_form = forms.RunConditionSubmitForm()

  if run_condition_form.validate_on_submit():
    synctasks.createRunConditionFromForm(app, run_condition_form, login.current_user)
    flash('success! run condition added to db', 'success')
  elif run_condition_form.is_submitted():
    print run_condition_form.errors
    flash('failure! run condition not added', 'failure')
    
  return render_template('form.html', form=run_condition_form)

@app.route("/scanrequestform", methods=('GET', 'POST'))
@login.login_required
def scan_request_form():
  scan_request_form = forms.ScanRequestSubmitForm()
  
  analysis  = dbmodels.Analysis.query.all()
  scan_request_form.analysis_choice.choices = [(str(a.id), a.id) for a in analysis]

  models = dbmodels.Model.query.all()
  scan_request_form.model_choice.choices = [(str(m.id), m.description_of_model) for m in models]
  
  requesters = dbmodels.User.query.all()
  scan_request_form.requester_choice.choices = [(str(r.id), r.name) for r in requesters]

  
  if scan_request_form.validate_on_submit():
    synctasks.createScanRequestFromForm(app, scan_request_form, login.current_user)
    flash('success!', 'success')
  elif scan_request_form.is_submitted():
    print scan_request_form.errors
    flash('failure!', 'failure')
    
  return render_template('form.html', form=scan_request_form)

@app.route("/pointrequestform", methods=('GET', 'POST'))
@login.login_required
def point_request_form():
  point_request_form = forms.PointRequestSubmitForm()
  
  models = dbmodels.Model.query.all()
  point_request_form.model_choice.choices = [(str(m.id), m.description_of_model) for m in models]
  
  scan_requests = dbmodels.ScanRequest.query.all()
  point_request_form.scan_request_choice.choices = [(str(s.id), s.id) for s in scan_requests]

  if point_request_form.validate_on_submit():
    synctasks.createPointRequestFromForm(app, point_request_form, login.current_user)
    flash('success!', 'success')
  elif point_request_form.is_submitted():
    print point_request_form.errors
    flash('failure!', 'failure')
    
    
  return render_template('form.html', form = point_request_form)

@app.route("/basicrequestform", methods=('GET', 'POST'))
@login.login_required
def basic_request_form():
  basic_request_form = forms.BasicRequestSubmitForm()
  
  
  if basic_request_form.validate_on_submit():
    synctasks.createBasicRequestFromForm(app, basic_request_form, login.current_user)
    flash('success!', 'success')
  elif basic_request_form.is_submitted():
    print basic_request_form.errors
    flash('failure!', 'failure')

  return render_template('form.html', form = basic_request_form)

# Views -------------------------------------------------------------------------------------
@app.route("/analyses")
@login.login_required
def analyses():
  query = db.session.query(dbmodels.Analysis).all()
  analyses = rows_to_dict(query)
  return render_template('viewer.html', rows = analyses, title= dbmodels.Analysis.__table__)

@app.route("/users")
@login.login_required
def users():
  query = db.session.query(dbmodels.User).all()
  users = rows_to_dict(query)
  return render_template('viewer.html', rows = users, title= dbmodels.User.__table__)


@app.route("/models")
@login.login_required
def models():
  query = db.session.query(dbmodels.Model).all()
  models = rows_to_dict(query)
  return render_template('viewer.html', rows = models, title= dbmodels.Model.__table__)

@app.route("/scanrequests")
@login.login_required
def scan_requests():
  query = db.session.query(dbmodels.ScanRequest).all()
  scanrequests = rows_to_dict(query)
  return render_template('viewer.html', rows = scanrequests, title= dbmodels.ScanRequest.__table__)

@app.route("/pointrequests")
@login.login_required
def point_requests():
  query = db.session.query(dbmodels.PointRequest).all()
  pointrequests = rows_to_dict(query)
  return render_template('viewer.html', rows = pointrequests, title = dbmodels.PointRequest.__table__)

@app.route("/basicrequests")
@login.login_required
def basic_requests():
  query = db.session.query(dbmodels.BasicRequest).all()
  basicrequests = rows_to_dict(query)
  return render_template('viewer.html', rows = basicrequests, title = dbmodels.BasicRequest.__table__)

@app.route("/links")
@login.login_required
def display_links():
  return render_template('links.html')

@app.route("/userstories")
@login.login_required
def display_user_stories():
  return render_template('userstories.html')

# Other functions ---------------------------------------------------------------------------
    
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


def rows_to_dict(rows):
  d = []
  for row in rows:
    new_dict = {}
    for column in row.__table__.columns:
      new_dict[column.name] = getattr(row, column.name)

    d.append(new_dict)
  
  return d
