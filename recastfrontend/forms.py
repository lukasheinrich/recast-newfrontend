from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

class AnalysisSubmitForm(Form):
    analysis_description = StringField('description', validators=[DataRequired()])
    run_condition_choice = SelectField('Run Conditions')

class UserSubmitForm(Form):
    name = StringField('user name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    
class ModelSubmitForm(Form):
    model_description = StringField('description', validators=[DataRequired()])
    
class RunConditionSubmitForm(Form):
    run_title = StringField('title of run condition', validators=[DataRequired()])

class ScanRequestSubmitForm(Form):
    description_of_model = StringField('description of model', validators=[DataRequired()])
    analysis_choice = SelectField('Select Analysis')
    model_choice = SelectField('Select Model')
    requester_choice = SelectField('Select User')

class PointRequestSubmitForm(Form):
    model_choice = SelectField('select model')
    scan_request_choice = SelectField('select request')

class BasicRequestSubmitForm(Form):
    number_of_events = IntegerField("Number of Events", validators=[DataRequired()])
    reference_cross_section = IntegerField("Reference cross section")
    conditions_description = IntegerField("Conditions description")
    #model = StringField('model')
    

class ScanResponseSubmitForm(Form):
    scan_request_choice = SelectField('Select scan request')
    model_choice = SelectField('Select model')
    

class PointResponseSubmitForm(Form):
    lumi_weighted_efficiency = StringField("Lumi weighted efficiency")
    total_luminosity = StringField("Total luminosity")
    l_1sig_limit_on_cs_wrt_ref = StringField("lower 1 sig limit on cross section")
    u_1sig_limit_on_cs_wrt_ref = StringField("Upper 1 sig limit on cross section")
    l_2sig_limit_on_cs_wrt_ref = StringField("lower 2 sig limit on cross section")
    u_2sig_limit_on_cs_wrt_ref = StringField("Upper 2 sig limit on cross section")
    log_likelihood_at_reference = StringField("Log likelihood at reference")
    #model = SelectField('Model')
    file_name = StringField("MergedTemplate: File name")
    file_path = StringField("MergedTemplate: File path")
    histo_name = StringField("MergedTemplate: Histogram name")
    histo_path = StringField("MergedTemplate: Histogram path")

class BasicResponseSubmitForm(Form):
    overall_efficiency = StringField("Overall efficiency")
    nominal_luminosity = StringField("nominal luminosity")
    l_1sig_limit_on_cs = StringField("lower 1 sig limit on cross section")
    u_1sig_limit_on_cs = StringField("Upper 1 sig limit on cross section")
    l_2sig_limit_on_cs = StringField("lower 2 sig limit on cross section")
    u_2sig_limit_on_cs = StringField("Upper 2 sig limit on cross section")
    l_1sig_limit_on_rate = StringField("lower 1 sig limit on rate")
    u_1sig_limit_on_rate = StringField("upper 1 sig limit on rate")
    l_2sig_limit_on_rate = StringField("lower 2 sig limit on rate")
    u_2sig_limit_on_rate = StringField("upper 2 sig limit on rate")
    log_likelihood_at_reference = StringField("log likelihood at reference")
    reference_cross_section = StringField("reference cross section")
    #model = SelectField('Model')
    file_name = StringField("SignalTemplate: File name")
    file_path = StringField("SignalTemplate: File path")
    histo_name = StringField("SignalTemplate: Histogram name")
    histo_path = StringField("SignalTemplate: Histogram path")
    


