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
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import re


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
ELASTIC_SEARCH_URL = frontendconf['ELASTIC_SEARCH_URL']
ELASTIC_SEARCH_INDEX = frontendconf['ELASTIC_SEARCH_INDEX']
ELASTIC_SEARCH_AUTH = frontendconf['ELASTIC_SEARCH_AUTH']
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
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
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
  
  confirmUserInDB(user)
  if not hasEmail(user):
    return redirect(url_for('signup'))
  
  return redirect(url_for('home'))
  

# Forms --------------------------------------------------------------------------------

def confirmUserInDB(user):
  try:
    user_query = dbmodels.User.query.filter(dbmodels.User.name == user.name()).one()
    confirmOrcid(user_query)
  except MultipleResultsFound, e:
    pass
  except NoResultFound, e:
    new_user = dbmodels.User(name=user.name(), email=None, orcid_id=user.get_id())
    db.session.add(new_user)
    db.session.commit()    
  return

def confirmOrcid(user_query):
  if not user_query.orcid_id:
    user_query.orcid_id = login.current_user.get_id()
    db.session.commit()

def hasEmail(user):
  try: 
    user_query = dbmodels.User.query.filter(dbmodels.User.name == user.name()).one()
    if not user_query.email:
      return False
  except MultipleResultsFound, e:
    pass
  except NoResultFound, e:
    pass

  return True

@app.route("/signup", methods=['GET', 'POST'])
def signup():
  form = forms.SignupSubmitForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      synctasks.createSignupFromForm(app, form, login.current_user)
      flash('success! form validated and was processed', 'success')
      return redirect(url_for('home'))
    elif form.is_submitted():
      print form.errors
      flash('failure! form did not validate and was not processed', 'danger')
    
  return render_template('signup.html', form=form)
    
  
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

@app.route("/editsubscription", methods=['GET', 'POST'], defaults={'id':0})
@app.route("/editsubscription/<int:id>", methods=['GET', 'POST'])
def edit_subscription(id):
  pass

@app.route("/editanalysis", methods=['GET', 'POST'], defaults={'id':0})
@app.route("/editanalysis/<int:id>", methods=['GET', 'POST'])
def edit_analysis(id):
  pass


@app.route("/editrequest", methods=['GET', 'POST'], defaults={'id':0})
@app.route("/editrequest/<int:id>", methods=['GET', 'POST'])
def edit_request(id):
  pass

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

      ''' Simple algorithm to gather the fields added dynamically 
           what we eventually want is to group all point_coordinate_X-y in the corresp. X's list
                where X is the parameter number and Y is the point coordinate(Axis)
      '''
      dict_value = {'1': 1} # for the initial parameter point, already present in WTForm
      for k in request.form.keys():
        if 'value_point_coordinate_' in k:
          #Get the Parameter number 
          #substring between last '_' and '-'
          parameter_number = int((re.search('coordinate_(.*)-', k)).group(1))
          if dict_value.has_key(str(parameter_number)):
            dict_value[str(parameter_number)] += 1
          else:
            dict_value[str(parameter_number)] = 1
            
        
      parameter_list = []
      for k, v in dict_value.iteritems():
        parameter = []
        i = 1
        if k == '1':
          parameter.append('value_point_coordinate')
          v -= 1
        while v > 0:
          value_id_name = 'value_point_coordinate_'+str(k)+'-'+str(i)
          if  request.form.has_key(value_id_name):
            parameter.append(value_id_name)
            v -= 1
          i += 1
        parameter_list.append(parameter)
      
      request_uuid = str(uuid.uuid1())
      deposition_id = synctasks.createDeposition(ZENODO_ACCESS_TOKEN,
                                                 request_uuid,
                                                 login.current_user,
                                                 request_form.reason_for_request.data,
                                                 request_form.title.data)
      
      request_form.uuid.data = request_uuid
      request_form.zenodo_deposition_id.data = deposition_id

      request_id = synctasks.createRequest(app, 
                                           request_form, 
                                           login.current_user)

      for parameter in parameter_list:
        print parameter
        #this is where I create a new Point request and retrieve its ID
        point_request_id = synctasks.createPointRequest(app,
                                                        request_id,
                                                        login.current_user)
        #Upload file on AWS and save into DB
        if parameter[0] == "value_point_coordinate":
          parameter_number = 1
          zip_file_form_name = 'zip_file'
        else:
          parameter_number = int((re.search('coordinate_(.*)-', parameter[0])).group(1))
          zip_file_form_name = 'zip_file_'+str(parameter_number)


        print zip_file_form_name
        zip_file = request.files[zip_file_form_name]
        
        file_uuid = str(uuid.uuid1())
        
        zip_file.save(zip_file.filename)
        
        synctasks.uploadToAWS(AWS_ACCESS_KEY_ID,
                              AWS_SECRET_ACCESS_KEY,
                              AWS_S3_BUCKET_NAME,
                              zip_file,
                              file_uuid)
        
        deposition_file_id = synctasks.uploadToZenodo(ZENODO_ACCESS_TOKEN,
                                                      deposition_id,
                                                      file_uuid,
                                                      zip_file)
        
        '''Uncomment when the website goes live'''
        #synctasks.publish(ZENODO_ACCESS_TOKEN,deposition_id)
                  
        synctasks.createRequestArchive(app,
                                       login.current_user,
                                       point_request_id,
                                       file_uuid,
                                       deposition_file_id,
                                       zip_file.filename)
        for coordinate in parameter:
          #Add each Point coordinate
          name_id_name = coordinate.replace("value", "name")
          coordinate_value = request.form[coordinate]
          coordinate_name = request.form[name_id_name]
          
          synctasks.createPointCoordinate(app,
                                          login.current_user,
                                          coordinate_name,
                                          coordinate_value,
                                          point_request_id)

      flash('success!', 'success')
      return redirect(url_for('analyses'))
  
    elif request_form.is_submitted():
      print request_form.errors
      flash(request_form.errors, 'failure')
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
  if request.args.has_key('sort'):
    query  = db.session.query(dbmodels.Analysis).order_by(dbmodels.Analysis.title).all()
    return render_template('analyses_views.html', analyses = query)

  if request.args.has_key('max_results'):
    pass

  query = db.session.query(dbmodels.Analysis).all()
  return render_template('analyses_views.html', analyses = query)


@app.route('/requests', methods=['GET', 'POST'])
@login.login_required
def requests_views():
  if request.args.has_key('sort'):
    query = db.session.query(dbmodels.ScanRequest).order_by(dbmodels.ScanRequest.title).all()
    return render_template('request_views.html', requests = query)

  query = db.session.query(dbmodels.ScanRequest).all()
  return render_template('request_views.html', requests = query)

@app.route('/request/<int:id>', methods=['GET', 'POST'])
@login.login_required
def request_view(id):  
  query = db.session.query(dbmodels.ScanRequest).filter(dbmodels.ScanRequest.id == id).all()
  return render_template('request.html', request = query[0], bucket_name=AWS_S3_BUCKET_NAME)

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

@app.route("/list-subscriptions-for-analysis", defaults={'analysis_id': 1})
@app.route("/list-subscriptions-for-analysis/<int:analysis_id>")
@login.login_required
def list_subscriptions(analysis_id):
  query = db.session.query(dbmodels.Subscription).filter(dbmodels.Subscription.analysis_id == analysis_id).all()
  
  return render_template('list_subscriptions.html', subscriptions = query)

@app.route("/list-requests-for-analysis", defaults={'analysis_id': 1})
@app.route("/list-requests-for-analysis/<int:analysis_id>")
@login.login_required
def list_requests(analysis_id):
  query = db.session.query(dbmodels.ScanRequest).filter(dbmodels.ScanRequest.analysis_id == analysis_id).all()
  return render_template('request_views.html', requests = query)

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

@app.route("/search", methods=['GET', 'POST', 'PUT'])
def search():
  q = request.args.get('q')

  if request.method == 'POST':
    q = request.form['q']
    doc_type = None
    print request.form['filter']
    if request.form['filter'] == 'Analysis':
      doc_type = 'analysis'
      search_data = synctasks.search(ELASTIC_SEARCH_URL,
                                     ELASTIC_SEARCH_AUTH,
                                     ELASTIC_SEARCH_INDEX,
                                     doc_type,
                                     q)
      ids = []
      for entry in search_data['hits']['hits']:
        ids.append(entry['_source']['id'])

      ids.sort()
      query = db.session.query(dbmodels.Analysis).filter(dbmodels.Analysis.id.in_(ids)).all()
      return render_template('analyses_views.html', analyses = query)
                   
    elif request.form['filter'] == 'Request':
      doc_type = 'requests'
      search_data = synctasks.search(ELASTIC_SEARCH_URL,
                                     ELASTIC_SEARCH_AUTH,
                                     ELASTIC_SEARCH_INDEX,
                                     doc_type,
                                     q)
      
      ids = [1,2,3,4]
      for entry in search_data['hits']['hits']:
        ids.append(entry['_source']['id'])            

      ids.sort()
      query = db.session.query(dbmodels.ScanRequest).filter(dbmodels.ScanRequest.id.in_(ids)).all()
      print len(query)
      return render_template('request_views.html', requests = query)

  return render_template('search.html', search_data=json.dumps(search_data['hits']['hits']))

def rows_to_dict(rows):
  d = []
  for row in rows:
    new_dict = {}
    for column in row.__table__.columns:
      new_dict[column.name] = getattr(row, column.name)

    d.append(new_dict)
  
  return d

@app.route("/arxiv", methods=['GET', 'POST'])
def arxiv():
  if request.args.has_key('id'):
    arxiv_id = request.args.get('id')
  print arxiv_id
  fields = "title,author,doi,abstract,corporate_name"
  url = "https://inspirehep.net/search?p={}&of=recjson&ot={}".format(arxiv_id,fields)
  print url
  response = requests.get(url)

  if not response.content or len(response.json()) > 1 or len(response.json()) == 0:
    """No record found"""
    return "{}"
  if len(response.json()) > 1:
    """More than one record found"""
    return "{N}"
  
  ret = response.json()[0]
  ret = json.dumps(ret)
  return ret
  
@app.route("/add-parameter/<int:request_id>", methods=['GET', 'POST'])
def add_parameter_point(request_id):
  coordinate = request.form['value']
  coordinate_name = request.form['name']
  zip_file = request.files['file']

  request_query = db.session.query(dbmodels.ScanRequest).filter(
    dbmodels.ScanRequest.id == request_id).one()

  file_uuid = str(uuid.uuid1())
  zip_file.save(zip_file.filename)

  synctasks.uploadToAWS(AWS_ACCESS_KEY_ID,
                        AWS_SECRET_ACCESS_KEY,
                        AWS_S3_BUCKET_NAME,
                        zip_file,
                        file_uuid)
    
  deposition_file_id = synctasks.uploadToZenodo(ZENODO_ACCESS_TOKEN,
                                                request_query.zenodo_deposition_id,
                                                file_uuid,
                                                zip_file)
  
  point_request_id = synctasks.createPointRequest(app,
                                                  request_id,
                                                  login.current_user
                                                  )

  synctasks.createPointCoordinate(app,
                                  login.current_user,
                                  coordinate_name,
                                  coordinate,
                                  point_request_id
                                  )

  synctasks.createRequestArchive(app,
                                 login.current_user,
                                 point_request_id,
                                 file_uuid,
                                 deposition_file_id,
                                 zip_file.filename)
  return ""



@app.route("/add-coordinate", methods=['GET', 'POST'])
@app.route("/add-coordinate/<int:point_request_id>", methods=['GET', 'POST'])
def add_coordinate(point_request_id):
  if request.method == 'POST':
    
    point_request_query = db.session.query(dbmodels.PointRequest).filter(
      dbmodels.PointRequest.id == point_request_id).one()


    data = json.loads(request.data.decode())
    coordinate = data['value']
    coordinate_name = data['name']
    point_coordinate_id = synctasks.createPointCoordinate(app,
                                                          login.current_user,
                                                          coordinate_name,
                                                          coordinate,
                                                          point_request_query.id)
    #return point_coordinate_id
    return ""

  return ""
           
@app.route("/analysis-number")
def analysis_number():
  analyses = db.session.query(dbmodels.Analysis).all()
  requests = db.session.query(dbmodels.ScanRequest).all()
  
  

  data = {}
  data['analyses'] = len(analyses)
  data['requests'] = len(requests)
  return jsonify(data)
