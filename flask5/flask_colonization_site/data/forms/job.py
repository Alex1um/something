from flask_wtf import *
from wtforms import *
from wtforms.validators import *


class JobForm(FlaskForm):

    job = StringField("Job title", validators=[DataRequired()])
    team_leader = StringField("Team leader id", validators=[DataRequired()])
    work_size = IntegerField("Work size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is finished?")
    submit = SubmitField("Submit")