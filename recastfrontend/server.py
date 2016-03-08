import json
import requests
import importlib
from boto3.session import Session

import asynctasks
import synctasks

from flask import Flask, redirect, jsonify, session, request, url_for, render_template, flash
from flask.ext import login as login
from frontendconfig import config as frontendconf
from recastdb.database import db
import recastdb.models as dbmodels
import forms
from werkzeug import secure_filename

import uuid

celeryapp  = importlib.import_module(frontendconf['CELERYAPP']).app

ORCID_APPID = frontendconf['ORCID_APPID']
ORCID_REDIRECT_URI = frontendconf['ORCID_REDIRECT_URI']
ORCID_SECRET = frontendconf['ORCID_SECRET']
ORCID_TOKEN_REDIRECT_URI = frontendconf['ORCID_TOKEN_REDIRECT_URI']
AWS_ACCESS_KEY_ID = frontendconf['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = frontendconf['AWS_SECRET_ACCESS_KEY']
ZENODO_CLIENT_ID = frontendconf['ZENODO_CLIENT_ID']
ZENODO_CLIENT_SECRET = frontendconf['ZENODO_CLIENT_SECRET']
ZENODO_ACCESS_TOKEN = frontendconf['ZENODO_ACCESS_TOKEN']
AWS_S3_BUCKET_NAME = 'recast'

ALLOWED_EXTENSIONS = set(['zip', 'txt'])

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
  print r
  print r.content
  login_details = json.loads(r.content)
  

  user = User(orcid = login_details['orcid'], fullname = login_details['name'], authenticated = True)
  login.login_user(user)

  return redirect(url_for('home'))

# Forms --------------------------------------------------------------------------------

def isUserInDB(user):
  user_query = dbmodels.User.query.filter(dbmodels.User.name == user.name()).all()
  assert len(user_query) < 2

  if (len(user_query)==0):
    new_user = User(name=user.name, email=None)
    db.session.add(new_user)
    db.session.commit()
    return False
  else :
     return (not user_query[0].email == None)  
    
  
@app.route("/analysis_form", methods=['GET', 'POST'])
@login.login_required
def form():
  #Analysis stuff
  myform = forms.AnalysisSubmitForm()
  run_condition_form = forms.RunConditionSubmitForm()

  collaborations = ['-None-', 'ATLAS', 'D0', 'CDF', 'CMS', 'ALEPH']
  myform.collaboration.choices = [(str(c), c) for i, c in enumerate(collaborations)]
  
  if myform.validate_on_submit():
    synctasks.createAnalysisFromForm(app,myform,login.current_user, run_condition_form)
    flash('success! form validated and was processed','success')
    return redirect(url_for('analyses'))

  elif myform.is_submitted():
    print myform.errors
    flash('failure! form did not validate and was not processed','danger')

  return render_template('analysis_form.html', form = myform, run_condition_form = run_condition_form)


@app.route("/userform", methods=['GET', 'POST'])
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

@app.route("/request_form", methods=['GET','POST'], defaults={'id': 1})
@app.route('/request_form/<int:id>', methods=['GET', 'POST'])
@login.login_required
def request_form(id):
  request_form = forms.RequestSubmitForm()
  
  parameter_point_form = forms.RequestParameterPointsSubmitForm()
  
  analysis = db.session.query(dbmodels.Analysis).filter(dbmodels.Analysis.id == id).all()
  request_form.analysis_id.data = analysis[0].id

  if request.method == 'POST':
    if request_form.validate_on_submit():
      lhe_file = request.files['lhe_file']
      if lhe_file:

        request_uuid = uuid.uuid1()
        file_uuid = uuid.uuid1()

        session = Session(
          aws_access_key_id=AWS_ACCESS_KEY_ID,
          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        lhe_file.save(lhe_file.filename)
        s3 = session.resource('s3')
        data = open(secure_filename(lhe_file.filename), 'rb')
        s3.Bucket(AWS_S3_BUCKET_NAME).put_object(Key=str(file_uuid), Body=data)
        
        #Upload to Zenodo test
        url = "https://zenodo.org/api/deposit/depositions/?access_token={}".\
            format(ZENODO_ACCESS_TOKEN)
        headers = {"Content-Type": "application/json"}
        description = "RECAST_request: {} \n Requester: {} ORCID: {} \n Request_description {}".\
            format(request_uuid, login.current_user.name(),
                   login.current_user.get_id(),
                   request_form.reason_for_request.data)

        deposition_data = {"metadata":
                       {
            "access_right": "embargoed",
            "upload_type": "dataset",
            "creators": [{"name": "Bora, Christian"}],
            "description": description,
            "title": "Sample title"
            }
                }
            
        print url
        print data
        response = requests.post(url, data=json.dumps(deposition_data), headers=headers)
        print response
        print response.content
        deposition_id = response.json()['id']
        
        url_deposition_file ="https://zenodo.org/api/deposit/depositions/{}/files?access_token={}".\
            format(deposition_id, ZENODO_ACCESS_TOKEN)
        json_data_file = {"filename": file_uuid}
        files = {'file': open(secure_filename(lhe_file.filename), 'rb')}
        response_file = requests.post(url_deposition_file, data=json_data_file, files=files)
        print response_file.content
        print response
        deposition_file_id = response_file.json()['id']

        request_form.zenodo_deposition_id.data = deposition_id
        request_form.uuid.data = request_uuid
        parameter_point_form.zenodo_file_id.data = deposition_file_id
        parameter_point_form.uuid.data = str(file_uuid)

      synctasks.createRequestFromForm(app, request_form, login.current_user, parameter_point_form)
      flash('success!', 'success')
      return redirect(url_for('analyses'))
  
    elif request_form.is_submitted():
      print request_form.errors
      flash('failure!', 'failure')
      filename = None
    
  return render_template('request_form.html', form=request_form,
                         parameter_points_form=parameter_point_form, analysis = analysis[0])
  
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

@app.route("/subscribe", methods=('GET', 'POST'), defaults={'id': 1})
@app.route('/subscribe/<int:id>')
@login.login_required
def subscribe(id):
  subscribe_form = forms.SubscribeSubmitForm()
  analysis = db.session.query(dbmodels.Analysis).filter(dbmodels.Analysis.id == id).all()
  subscribe_form.analysis_id.data = analysis[0].id

  if subscribe_form.validate_on_submit():
    synctasks.createSubscriptionFromForm(app, subscribe_form, login.current_user)
    flash('success! You have been subscribed', 'success')
    return redirect(url_for('analyses'))
  elif subscribe_form.is_submitted():
    flash('failure!', 'failure')

  return render_template('subscribe.html', form=subscribe_form, analysis = analysis[0])
  
@app.route("/contact", methods=('GET', 'POST'), defaults={'id': 1})
@app.route('/contact/<int:id>')
@login.login_required
def contact(id):
  contact_form = forms.ContactSubmitForm()
  user = db.session.query(dbmodels.User).filter(dbmodels.User.name == login.current_user.name()).all()
  contact_form.responder.data = user[0].name
  contact_form.responder_email.data = user[0].email

  return render_template('contact.html', form = contact_form)

# Views -------------------------------------------------------------------------------------
@app.route("/analysis/<int:id>", methods=['GET', 'POST'])
def analysis(id):
  query = db.session.query(dbmodels.Analysis).filter(dbmodels.Analysis.id == id).all()
  return render_template('analysis.html', analysis=query[0])

@app.route("/analyses", methods=['GET', 'POST'])
@login.login_required
def analyses():
  query = db.session.query(dbmodels.Analysis).all()
  return render_template('analyses_views.html', analyses = query)


@app.route('/requests', methods=['GET', 'POST'])
@login.login_required
def requests_views():
  query = db.session.query(dbmodels.ScanRequest).all()
  return render_template('request_views.html', requests = query)

@app.route('/request/<int:id>', methods=['GET', 'POST'])
@login.login_required
def request_view(id):
  query = db.session.query(dbmodels.ScanRequest).filter(dbmodels.ScanRequest.id == id).all()
  return render_template('request.html', request = query[0])

@app.route('/subscriptions')
@login.login_required
def subscriptions():
  query = db.session.query(dbmodels.Subscription).all()
  return render_template('subscriptions.html', subscriptions = query)

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

@app.route("/testing", defaults={'page': 1})
@app.route('/testing/page/<int:page>')
@login.login_required
def display_testing(page):
  query = db.session.query(dbmodels.Analysis).all()
  count = len(query)
  new_query = get_elements_for_page(page, 5, count, query)
  
  if not new_query and page != 1:
    #abort(404)
    pass
  
  #pagination = Pagination(page=page, total=count)
  #return render_template('testing.html', analyses = new_query, pagination = pagination)
  return render_template('testing.html', analyses = new_query)

@app.route("/list_subscriptions", defaults={'analysis_id': 1})
@app.route("/list_subscriptions/analysis/<int:analysis_id>")
@login.login_required
def list_subscriptions(analysis_id):
  query = db.session.query(dbmodels.Subscription).filter(dbmodels.Subscription.analysis_id == analysis_id).all()
  
  return render_template('list_subscriptions.html', subscriptions = query)

@app.route("/list_requests", defaults={'analysis_id': 1})
@app.route("/list_requests/analysis/<int:analysis_id>")
@login.login_required
def list_requests(analysis_id):
  query = db.session.query(dbmodels.ScanRequest).filter(dbmodels.ScanRequest.analysis_id == analysis_id).all()

  return render_template('list_requests.html', requests = query)


def get_elements_for_page(page, PER_PAGE, count, obj):
  first_index = (page - 1) * PER_PAGE
  last_index = first_index + PER_PAGE
  return obj[first_index:last_index]


def url_for_other_page(page):
  args = request.view_args.copy
  args['page'] = page
  return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_pages'] = url_for_other_page
  
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

@app.route("/profile", methods=['GET', 'POST'])
@login.login_required
def profile():
  user_query = dbmodels.User.query.filter(dbmodels.User.name == login.current_user.name()).all()
  assert len(user_query)

  if request.method == 'POST':
    token = dbmodels.AccessToken.query.filter(dbmodels.AccessToken.id == request.form['delete']).one()
    db.session.delete(token)
    db.session.commit()

  return render_template('profile.html', db_user = user_query[0], tokens=user_query[0].access_tokens)

@app.route("/token", methods=['GET', 'POST'])
@login.login_required
def show_token():  
  user_query = dbmodels.User.query.filter(dbmodels.User.name == login.current_user.name()).all()
  assert len(user_query)
  
  if request.method == 'POST':
    new_token = dbmodels.AccessToken(token_name=request.form['tokenname'], user_id=user_query[0].id)
    db.session.add(new_token)
    db.session.commit()
  elif request.method == 'GET':
    tokens = db.session.query(dbmodels.AccessToken).all()
    new_token = tokens[len(tokens)-1]
                                     
  if not request.args.has_key('code'):
    return  redirect('https://orcid.org/oauth/authorize?client_id={}&response_type=code&scope=/authenticate&redirect_uri={}&show_login=true'.format(
    ORCID_APPID,
    ORCID_TOKEN_REDIRECT_URI
  ))
  
  auth_code = request.args.get('code')
  data = {'client_id':ORCID_APPID,'client_secret':ORCID_SECRET,'grant_type':'authorization_code','code':auth_code, 'redirect_uri':ORCID_TOKEN_REDIRECT_URI}

  r = requests.post('https://pub.orcid.org/oauth/token', data = data)
  login_details = json.loads(r.content)


  if not user_query[0].orcid_id:
    user_query[0].orcid_id = login_details['orcid']
    db.session.add(user_query[0])
    db.session.commit()
  
  new_token.token = login_details['access_token']
  db.session.add(new_token)
  db.session.commit()
  return render_template('new_token.html', token=new_token, user=user_query[0])

def rows_to_dict(rows):
  d = []
  for row in rows:
    new_dict = {}
    for column in row.__table__.columns:
      new_dict[column.name] = getattr(row, column.name)

    d.append(new_dict)
  
  return d
