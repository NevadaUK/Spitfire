from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Spitfire1 import db
from Spitfire1.groups.forms import CreateGroupForm
from Spitfire1.models import User, Group
import secrets

groups = Blueprint("groups", __name__)


@groups.route("/creategroup", methods=["GET", "POST"])
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
