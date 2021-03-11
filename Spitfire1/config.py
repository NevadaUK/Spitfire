import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "136857bafd97dfce1f0c2bf8e4e620a3")
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "spitfireappemail@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    UPLOAD_FOLDER = "static/group_files"


    SQLALCHEMY_TRACK_MODIFICATIONS = False
