from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint, current_app, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from Spitfire1 import db
from Spitfire1.models import User, Group, Task, Comments, Files
from Spitfire1.dash.forms import TaskForm, EditTaskForm, CommentForm, UploadFileForm
from werkzeug.utils import secure_filename
import os
from flask import current_app

dash = Blueprint("dash", __name__)


@dash.route("/dashboard/group/<int:group_id>", methods=["GET", "POST"])
@login_required
def taskview(group_id):
    if current_user.group_id == 0:
        return redirect(url_for("groups.creategroup"))
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    tasks = Task.query.filter_by(group_id=group_id.id, completed=False).order_by(
        Task.date_posted.desc()
    )
    tasksall = Task.query.filter_by(group_id=group_id.id)
    tasksnotcomlpeted = tasksall.filter_by(completed=False)
    if tasksall.count() == 0:
        taskpercentage = 100
    else:
        taskpercentage = tasksnotcomlpeted.count()/tasksall.count()*100
    ammount = User.query.filter_by(group_id=current_user.group_id)
    return render_template(
        "dashboard.html",
        group_id=group_id,
        tasks=tasks,
        ammount=ammount,
        title="Dashboard",
        comments = Comments,
        files = Files,
        taskpercentage = int(taskpercentage)
    )


@dash.route("/dashboard/group/<int:group_id>/completed", methods=["GET", "POST"])
@login_required
def taskviewcompleted(group_id):
    if current_user.group_id == 0:
        return redirect(url_for("groups.creategroup"))
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    users = User.query.filter_by(group_id=current_user.group_id)
    tasks = Task.query.filter_by(group_id=group_id.id, completed=True).order_by(
        Task.date_posted.desc()
    )
    tasksall = Task.query.filter_by(group_id=group_id.id)
    tasksnotcomlpeted = tasksall.filter_by(completed=False)
    if tasksall.count() == 0:
        taskpercentage = 100
    else:
        taskpercentage = tasksnotcomlpeted.count()/tasksall.count()*100
    ammount = User.query.filter_by(group_id=current_user.group_id)
    return render_template(
        "dashboard2.html",
        group_id=group_id,
        tasks=tasks,
        ammount=ammount,
        title="Dashboard",
        comments = Comments,
        files = Files,
        taskpercentage = int(taskpercentage)
    )


@dash.route("/dashboard/group/<int:group_id>/new_task", methods=["GET", "POST"])
@login_required
def new_task(group_id):
    # if current_user.id != 1:
    # abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            TaskName=form.title.data,
            content=form.content.data,
            author=current_user,
            group_id=current_user.group_id,
            completed=False,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task Created.", "success")
        return redirect(url_for("dash.taskview", group_id=current_user.group_id))
    return render_template(
        "createtask.html", title="Create a new task", form=form, legend="New Task"
    )


@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>", methods=["POST", "GET"]
)
@login_required
def viewtask(task_id, group_id):
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    task = Task.query.get_or_404(task_id)
    if task.completed == True:
        return redirect(url_for("dash.taskview", group_id=current_user.group_id))
    page = request.args.get("page", 1, type=int)
    comments = Comments.query.filter_by(group_id=current_user.group_id, task_id=task_id).order_by(Comments.date_posted.desc()).paginate(page=page, per_page=1)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(
            content=form.content.data, author=current_user, task_id=task_id, group_id=current_user.group_id
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment Created.", "success")
        return redirect(url_for("dash.taskview", group_id=current_user.group_id))
    return render_template("task.html", title=task.TaskName, task=task, form=form, comments=comments)

@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/comments", methods=["POST", "GET"]
)
@login_required
def comments(task_id, group_id):
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    task = Task.query.get_or_404(task_id)
    page = request.args.get("page", 1, type=int)
    comments = Comments.query.filter_by(group_id=current_user.group_id, task_id=task_id).order_by(Comments.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("comments.html", title=task.TaskName + " - Comments", task=task, comments=comments, group_id=current_user.group_id, task_id=task_id)

@dash.route(
    "/dashboard/group/<int:group_id>/completed/task/<int:task_id>",
    methods=["POST", "GET"],
)
@login_required
def viewtaskcompleted(task_id, group_id):
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    task = Task.query.get_or_404(task_id)
    if task.completed == False:
        return redirect(url_for("dash.taskviewcompleted", group_id=current_user.group_id))
    page = request.args.get("page", 1, type=int)
    comments = Comments.query.filter_by(group_id=current_user.group_id, task_id=task_id).order_by(Comments.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template("task2.html", title=task.TaskName, task=task, comments=comments)


@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/setascompleted",
    methods=["POST", "GET"],
)
@login_required
def task_markascomplete(task_id, group_id):
    task = Task.query.get_or_404(task_id)
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    if task.author != current_user:
        abort(403)
    task.completed = True
    db.session.commit()
    flash("Set as Completed.", "success")
    return redirect(url_for("dash.taskviewcompleted", group_id=current_user.group_id))


@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/setasuncompleted",
    methods=["POST", "GET"],
)
@login_required
def task_markasuncomplete(task_id, group_id):
    task = Task.query.get_or_404(task_id)
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    if task.author != current_user:
        abort(403)
    task.completed = False
    db.session.commit()
    flash("Set as Uncompleted.", "danger")
    return redirect(url_for("dash.taskviewcompleted", group_id=current_user.group_id))


@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/edit", methods=["GET", "POST"]
)
@login_required
def update_task(task_id, group_id):
    task = Task.query.get_or_404(task_id)
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    if task.author != current_user:
        abort(403)
    form = EditTaskForm()
    if form.validate_on_submit():
        task.TaskName = form.title.data
        task.content = form.content.data
        db.session.commit()
        flash("Task Edited.", "success")
        return redirect(
            url_for("dash.taskview", task_id=task.id, group_id=current_user.group_id)
        )
    elif request.method == "GET":
        form.title.data = task.TaskName
        form.content.data = task.content
    return render_template(
        "edittask.html", title="Edit Task", form=form, legend="Edit Post"
    )


@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/delete", methods=["POST"]
)
@login_required
def delete_task(task_id, group_id):
    task = Task.query.get_or_404(task_id)
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task Deleted.", "danger")
    return redirect(url_for("dash.taskview", group_id=current_user.group_id))

@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/files", methods=["POST", "GET"]
)
@login_required
def viewfiles(task_id, group_id):
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    task = Task.query.get_or_404(task_id)
    files = Files.query.filter_by(group_id=current_user.group_id, task_id=task.id).order_by(Files.date_posted.desc())
    return render_template("FileView.html", title=task.TaskName + " - Files", task=task, files=files, task_id=task.id, User=User)


@dash.route("/dashboard/group/<int:group_id>/task/<int:task_id>/fileupload", methods=["GET", "POST"])
@login_required
def uploadfile(group_id, task_id):
    task = Task.query.get_or_404(task_id)
    form = UploadFileForm()
    if form.validate_on_submit():
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join(current_app.root_path, "static/group_files", filename))
            file = Files(
                file_name=filename,
                user_id=current_user.id,
                task_id=task.id,
                group_id=current_user.group_id,
            )
            db.session.add(file)
            db.session.commit()
        flash("File Uploaded.", "success")
        return redirect(url_for("dash.viewtask", group_id=current_user.group_id, task_id=task_id))
    return render_template("uploadfile.html", title="Upload File", form=form, legend="Upload File", task=task)

@dash.route(
    "/dashboard/group/<int:group_id>/task/<int:task_id>/files/download/<string:filename>", methods=["POST", "GET"]
)
@login_required
def downloadfile(task_id, group_id, filename):
    group_id = Group.query.filter_by(id=current_user.group_id).first_or_404()
    task = Task.query.get_or_404(task_id)
    location = os.path.join(current_app.root_path, "static/group_files")
    return send_from_directory(directory=location, filename=filename, as_attachment=True)

@dash.route(
    "/dashboard/group/<int:group_id>/viewusers", methods=["POST", "GET"]
)
@login_required
def viewusers(group_id):
    group = Group.query.filter_by(id=current_user.group_id).first_or_404()
    users = User.query.filter_by(group_id=current_user.group_id).order_by(User.id.desc())
    return render_template("listusers.html", title=group.groupname + " - Users", group_id=current_user.group_id, group=group, users=users)
