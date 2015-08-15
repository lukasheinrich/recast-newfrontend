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

