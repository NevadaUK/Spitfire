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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Spitfire Password Reset Request', sender='spitfireappemail@gmail.com', recipients=[user.email])
    msg.body = f''' Reset Password Link.
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then ignore this email.
'''
    mail.send(msg)
