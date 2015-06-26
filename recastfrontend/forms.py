from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class AnalysisSubmitForm(Form):
    analysis_description = StringField('description', validators=[DataRequired()])
    run_condition_choice = SelectField('Run Conditions')