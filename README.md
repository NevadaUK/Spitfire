# Spitfire
## Install Process
```shell
git clone https://github.com/NevadaUK/Spitfire
cd Spitfire
pip install poetry
poetry install
poetry run flask db init

poetry run flask run
```


Dependencies
- Flask
- flask_mail
- Pillow
- SQLAlchemy
- flask-bcrypt
- flask_login 
- flask_migrate 
- wtforms
- flask_wtf
- email_validator
- itsdangerous

To Do
- Comment System
- File Upload for Tasks
