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

# Response tables --------------------------------------------------------------------------

def createScanResponseFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    assert len(user_query) == 1

    scan_response = dbmodels.ScanResponse(model_id = int(form.model_choice.data),
                                          scan_request_id = int(form.scan_request_choice.data)
                                          )    
    db.session.add(scan_response)
    db.session.commit()
                                                            
    
def createPointResponseFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    
    assert len(user_query) == 1
    histo = dbmodels.Histogram(file_name = form.file_name.data,
                               file_path = form.file_path.data,
                               histo_name = form.histo_name.data,
                               histo_path = form.hist_path.data
                               )

    point_response = dbmodels.PointResponse(lumi_weighted_efficiency = form.lumi_weighted_efficiency.data,
                                            total_luminosity = form.total_luminosity.data,
                                            lower_1sig_limit_on_cross_section_wrt_reference = form.l_1sig_limit_on_cs_wrt_ref.data,
                                            upper_1sig_limit_on_cross_section_wrt_reference = form.u_1sig_limit_on_cs_wrt_ref.data,
                                            lower_2sig_limit_on_cross_section_wrt_reference = form.l_2sig_limit_on_cs_wrt_ref.data,
                                            upper_2sig_limit_on_cross_section_wrt_reference = form.u_2sig_limit_on_cs_wrt_ref.data,
                                            log_likelihood_at_reference = form.log_likelihood_at_reference.data,
                                            merged_signal_template_wrt_reference = [histo]
                                            )
    

    db.session.add(histo)
    db.session.add(point_response)
    db.session.commit()
    


def createBasicResponseFromForm(app, form, current_user):
  with app.app_context():
    user_query = dbmodels.User.query.filter(dbmodels.User.name == current_user.name()).all()
    
    assert len(user_query) == 1
    
    histo = dbmodels.Histogram(file_name = form.file_name.data,
                               file_path = form.file_path.data,
                               histo_name = form.histo_name.data,
                               histo_path = form.histo_path.data
                               )

    basic_response = dbmodels.BasicResponse(overall_efficiency = form.overall_efficiency.data,
                                            nominal_luminosity = form.nominal_luminosity.data,
                                            lower_1sig_limit_on_cross_section = form.l_1sig_limit_on_cs.data,
                                            upper_1sig_limit_on_cross_section = form.u_1sig_limit_on_cs.data,
                                            lower_2sig_limit_on_cross_section = form.l_2sig_limit_on_cs.data,
                                            upper_2sig_limit_on_cross_section = form.u_2sig_limit_on_cs.data,
                                            lower_1sig_limit_on_rate = form.l_1sig_limit_on_rate.data,
                                            upper_1sig_limit_on_rate = form.u_1sig_limit_on_rate.data,
                                            lower_2sig_limit_on_rate = form.l_2sig_limit_on_rate.data,
                                            upper_2sig_limit_on_rate = form.u_2sig_limit_on_rate.data,
                                            log_likelihood_at_reference = form.log_likelihood_at_reference.data,
                                            reference_cross_section = form.reference_cross_section.data,
                                            signal_template = [histo]
                                            )
    
    db.session.add(histo)
    db.session.add(basic_response)
    db.session.commit()
