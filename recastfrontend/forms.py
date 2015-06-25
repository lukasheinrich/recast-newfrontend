from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class AnalysisSubmitForm(Form):
    analysis_name = StringField('analysis name', validators=[DataRequired()])
    analysis_description = StringField('description', validators=[DataRequired()])