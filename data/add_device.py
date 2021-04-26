from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddDeviceForm(FlaskForm):
    device = StringField('Device', validators=[DataRequired()])
    creator = StringField('Creator', validators=[DataRequired()])
    users = StringField('Users', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    is_working = BooleanField('Is working?')

    submit = SubmitField('Submit')
