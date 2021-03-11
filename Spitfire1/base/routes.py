from flask import Blueprint, render_template, request
from Spitfire1 import db
from Spitfire1.models import Post

base = Blueprint("base", __name__)


@base.route("/about")
def about():
    return render_template("about.html", title="About")


@base.route("/")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template(
        "homepage.html", posts1=posts[0], posts2=posts[1], posts3=posts[2]
    )

@base.route("/TermsandConditions")
def TsandCs():
    return render_template("termsandconditions.html", title="About")

@base.route("/PrivacyPolicy")
def PrivPol():
    return render_template("privacypolicy.html", title="About")
