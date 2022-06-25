import wtforms
from wtforms.fields import *
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateField, RadioField, FieldList, FormField
from wtforms.validators import DataRequired, InputRequired, Optional
from flask_wtf import FlaskForm, Form
# from wtforms.fields.html5 import DateFi
from datetime import date


class CheckRain(FlaskForm):
    address = StringField('Enter a City and State OR Zip Code',default='Chicago, IL', validators=[DataRequired()])
    start_date = DateField('Date From', default=date.today())
    end_date = DateField('Date to', default=date.today())

    submit = SubmitField("Get Rainfall Total")