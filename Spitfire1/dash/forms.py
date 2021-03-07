from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    TextAreaField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from flask_login import current_user
from Spitfire1.models import User, Group


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Update Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class EditTaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Update Content", validators=[DataRequired()])
    files = MultipleFileField("Files")
    submit = SubmitField("Post")
