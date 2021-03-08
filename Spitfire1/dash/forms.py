from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
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
    content = TextAreaField("Task Content and Instructions", validators=[DataRequired()])
    submit = SubmitField("Post")


class EditTaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Update Content", validators=[DataRequired()])
    files = MultipleFileField("Files")
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    content = TextAreaField("Add Comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")

class UploadFileForm(FlaskForm):
    file = FileField("Attach Files", validators=[FileRequired()])
    submit = SubmitField("Upload")
