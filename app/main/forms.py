from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Not Applied', 'Not Applied'),
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected')
    ], validators=[DataRequired()])
    deadline = DateField('Application Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit') 