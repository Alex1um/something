from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import EmailField


class DepartForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    chief = IntegerField("Chief", validators=[DataRequired()])
    members = StringField("Members")
    email = EmailField("Email", validators=[Email(), data_required()])
    submit = SubmitField("Submit")