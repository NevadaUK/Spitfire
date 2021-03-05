import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from Spitfire1 import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_images', picture_filename)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(image_path)

    return picture_filename
