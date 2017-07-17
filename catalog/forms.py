from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class itemForm(Form):
    # TO DO:
    # Select category dynamically from database - load all form database and populate,m
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description')
    category