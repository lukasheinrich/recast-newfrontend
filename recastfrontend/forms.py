from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, FormField, SubmitField, FieldList, FileField
from wtforms.validators import DataRequired

class RunConditionSubmitForm(Form):
    name  = StringField('Title of run condition', validators=[DataRequired()])
    description = TextAreaField('Description')

class AnalysisSubmitForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    collaboration = SelectField('Collaboration')
    e_print = StringField('E print')
    journal = StringField('Journal')
    doi = StringField('DOI')
    inspire_URL = StringField('URL')
    description = TextAreaField('Description')

class UserSubmitForm(Form):
    name = StringField('user name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    
class ModelSubmitForm(Form):
    model_description = StringField('description', validators=[DataRequired()])
    
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

class RequestSubmitForm(Form):
    analysis = SelectField('Analysis', validators=[DataRequired()])
    model_name = StringField('Model Name', validators=[DataRequired()])
    reason_for_request = TextAreaField('Reason for request')
    additional_information = TextAreaField('Additional information')

class RequestParameterPointsSubmitForm(Form):
    parameter_point = StringField('Parameter Point 1', validators=[DataRequired()])
    lhe_file = FileField('LHE file', validators=[DataRequired()])
    number_events = IntegerField('# of events')
    reference_cross_section = StringField('Reference cross section')
