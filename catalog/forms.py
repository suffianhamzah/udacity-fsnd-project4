from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class itemForm(FlaskForm):
    """Form for creating and editing items"""
    name = StringField('Name', validators=[DataRequired(), Length(max=250)])
    description = TextAreaField('Description', validators=[Optional()])
    category = SelectField('Category', coerce=int)
