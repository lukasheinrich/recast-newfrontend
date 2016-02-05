import recastdb.models as dbmodels
from recastdb.database import db

def createAnalysisFromForm(app,form,current_user, run_condition_form):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query)==1
    run_condition = dbmodels.RunCondition(name = run_condition_form.name.data,
                                          description = run_condition_form.description.data
                                          )
    
    db.session.add(run_condition)
    db.session.commit()

    analysis = dbmodels.Analysis(owner_id = user_query[0].id,
                                 title = form.title.data,
                                 collaboration = form.collaboration.data,
                                 e_print = form.e_print.data,
                                 journal = form.journal.data,
                                 doi = form.doi.data,
                                 inspire_URL = form.inspire_URL.data,
                                 description = form.description.data,
                                 run_condition_id = run_condition.id
                                 )

    db.session.add(analysis)
    db.session.commit()
    

def createUserFromForm(app, form):
  with app.app_context():
    user = dbmodels.User(name = form.name.data, email = form.email.data)

    db.session.add(user)
    db.session.commit()

def createModelFromForm(app, form, current_user):
  with app.app_context():

    model = dbmodels.Model(form.model_description.data)
    db.session.add(model)
    db.session.commit()

def createRunConditionFromForm(app, form, current_user):
  with app.app_context():
    run_condition = dbmodels.RunCondition(name = form.name.data,
                                          description = form.description.data
                                          )

    db.session.add(run_condition)
    db.session.commit()


# Request tables --------------------------------------------------------------------------
def createRequestFromForm(app, request_form, current_user, parameter_points_form):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query)==1
    
    scan_request = dbmodels.ScanRequest(requester_id = user_query[0].id,
                                        reason_for_request = request_form.reason_for_request.data,
                                        additional_information = request_form.additional_information.data,
                                        analysis_id = request_form.analysis_id.data
                                        )

    db.session.add(scan_request)
    db.session.commit()
    
    
    point_request = dbmodels.PointRequest(requester_id = user_query[0].id,
                                          scan_request_id = scan_request.id
                                          )

    db.session.add(point_request)
    db.session.commit()

    basic_request = dbmodels.BasicRequest(number_of_events = parameter_points_form.number_events.data,
                                          reference_cross_section = parameter_points_form.reference_cross_section.data,
                                          requester_id = user_query[0].id,
                                          point_request_id = point_request.id
                                          )

    db.session.add(basic_request)
    db.session.commit()

    parameter_point = dbmodels.ParameterPoint(value = parameter_points_form.parameter_point.data,
                                              point_request_id = point_request.id
                                              )
    db.session.add(parameter_point)
    db.session.commit()


    lhe_file = dbmodels.LHEFile(file_name = parameter_points_form.lhe_file.data,
                                path = './',
                                basic_request_id = basic_request.id
                                )
    db.session.add(lhe_file)
    db.session.commit()
                                
    
    
def createScanRequestFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query)==1

    request = dbmodels.ScanRequest(requester_id = int(form.requester_choice.data),
                                   model_id = int(form.model_choice.data),
                                   analysis_id = int(form.analysis_choice.data),
                                   description_of_model = form.description_of_model.data
                                   )
    
    db.session.add(request)
    db.session.commit()


def createPointRequestFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    
    assert len(user_query) == 1
    
    point_request = dbmodels.PointRequest(model_id = int(form.model_choice.data),
                                          scan_request_id = int(form.scan_request_choice.data),
                                          requester_id = user_query[0].id
                                          )
    
    db.session.add(point_request)
    db.session.commit()
    

def createBasicRequestFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query) == 1
    
    basic_request = dbmodels.BasicRequest(number_of_events = form.number_of_events.data,
                                          reference_cross_section = form.reference_cross_section.data,
                                          conditions_description = form.conditions_description.data,
                                          requester_id = user_query[0].id
                                          )
    db.session.add(basic_request)
    db.session.commit()


def createSubscriptionFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query) == 1

    subscription = dbmodels.Subscription(subscription_type = form.subscription_type.data,
                                          description = form.description.data,
                                          requirements = form.requirements.data,
                                          notifications = '\n'.join(form.notifications.data),
                                          subscriber_id = user_query[0].id,
                                          analysis_id = form.analysis_id.data
                                          )
    db.session.add(subscription)
    db.session.commit()
