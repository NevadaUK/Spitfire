from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from Spitfire1 import db
from Spitfire1.models import Post
from Spitfire1.posts.forms import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/news")
def news():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template("news.html", posts=posts, title="News")


@posts.route("/postnews/new", methods=["GET", "POST"])
@login_required
def new_post():
    if current_user.id != 1:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Post Created.", "success")
        return redirect(url_for("posts.news"))
    return render_template(
        "create_post.html", title="New Post to Updates", form=form, legend="New Post"
    )


@posts.route("/postnews/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/postnews/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Edited.", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Edit Post", form=form, legend="Edit Post"
    )


@posts.route("/postnews/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted.", "danger")
    return redirect(url_for("posts.news"))
