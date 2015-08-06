import recastdb.models as dbmodels
from recastdb.database import db

def createAnalysisFromForm(app,form,current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query)==1
    

    analysis = dbmodels.Analysis(owner_id = user_query[0].id,
        description_of_original_analysis = form.analysis_description.data,
        run_condition_id = int(form.run_condition_choice.data)
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

    run_condition = dbmodels.RunCondition(title = form.run_title.data)

    db.session.add(run_condition)
    db.session.commit()


# Request tables --------------------------------------------------------------------------

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
