from flask_wtf import *
from wtforms import *
from wtforms.validators import *


class LoginForm(FlaskForm):
    login = StringField("Login / email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField("Submit")
