"""
this file will be imported by the __init__.py in the same directory
It will first try to read from the environment variables, so
`export SECRET_KEY='yourkey` would override the settings below.
Also `export DATABASE_URL='postgresql://usernam:password@database.example.com
        :5432/your_db'`

NOTE: you could also do something like this, having more environment variables/

SQLALCHEMY_DATABASE_URI =
        f"postgresql://{os.environ['DATABASE_USERNAME']}:
            {os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}
            :{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"

Below, I do a variation.

NOTE: this could also be created as on object, and read in the
     __init__.py  with
    `app.config.from_object(Config)

"""
import os

DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME') or 'postgres'
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or ''
DATABASE_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
DATABASE_PORT = os.environ.get('DATABASE_PORT') or '5432'
DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'moody'

# form string differently  if there's a password
if DATABASE_PASSWORD:
    db_user = f"{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
else:
    db_user = DATABASE_USERNAME

database_url_string = \
    f"postgresql://{db_user}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# put it all together
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or database_url_string

# other settings from examples.
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
FLASK_DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
