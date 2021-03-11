from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from flask_login import current_user
from Spitfire1.models import User, Group


class CreateGroupForm(FlaskForm):
    groupname = StringField(
        "Group Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    group_id = IntegerField("Group ID", validators=[DataRequired()])
    submit = SubmitField("Create Group")

    def validate_groupname(self, groupname):
        group = Group.query.filter_by(groupname=groupname.data).first()
        if group:
            raise ValidationError("Group Name already exists.")

    def validate_groupID(self, group_id):
        groupid = Group.query.filter_by(group_id=group_id.data).first()
        if groupid:
            raise ValidationError("A Group with that ID already exists.")

class JoinGroupForm(FlaskForm):
    group_id = IntegerField("Group ID", validators=[DataRequired()])
    submit = SubmitField("Join Group")

    def validate_groupID(self, group_id):
        groupid != Group.query.filter_by(group_id=group_id.data).first()
        if groupid:
            raise ValidationError("Group doesn't exist.")
