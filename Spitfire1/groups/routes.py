from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Spitfire1 import db
from Spitfire1.groups.forms import CreateGroupForm, JoinGroupForm
from Spitfire1.models import User, Group
import secrets

groups = Blueprint("groups", __name__)


@groups.route("/creategroup", methods=["GET", "POST"])
@login_required
def creategroup():
    if current_user.is_authenticated and current_user.group_id != 0:
        return redirect(url_for("base.home"))
    form = CreateGroupForm()
    random_hex = secrets.token_hex(8)
    if form.validate_on_submit():
        group = Group(
            groupname=form.groupname.data, id=form.group_id.data, joincode=random_hex
        )
        db.session.add(group)
        current_user.group_id = form.group_id.data
        db.session.commit()
        flash(f"Group {form.groupname.data} Created!", "success")
        return redirect(url_for("base.home"))
    return render_template("creategroup.html", title="Create Group", form=form)

@groups.route("/joingroup", methods=["GET", "POST"])
@login_required
def joingroup():
    if current_user.is_authenticated and current_user.group_id != 0:
        return redirect(url_for("base.home"))
    form = JoinGroupForm()
    if form.validate_on_submit():
        current_user.group_id = form.group_id.data
        db.session.commit()
        flash(f"Group Joined!", "success")
        return redirect(url_for("users.account"))
    return render_template("joingroup.html", title="Join Group", form=form)
