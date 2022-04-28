from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class SearchForm(FlaskForm):
    search = SubmitField(validators=[DataRequired()])
