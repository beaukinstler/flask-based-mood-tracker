# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
from src import login_manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
# from sqlalchemy import Index
import datetime
from src.security import pwd_context
from src import db
from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.sql.expression import func
from pytz import timezone




class UserMoodLog(db.Model):
    """
    found example here https://gist.github.com/asyd/3cff61ed09eabe187d3fbec2c8a3ee39
    but it's for a class, to guessed on the syntax.
    """

    __tablename__ = 'users_moods'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=False)
    mood_id = db.Column('mood_id', db.Integer, db.ForeignKey(
        'moods.id'), primary_key=False)
    created_at = db.Column(db.DateTime,
                           default=func.now())
    note = db.Column("notes", db.Text, nullable=True)
    user = db.relationship('User', back_populates="moods", cascade="all, delete")
    mood = db.relationship('Mood', back_populates="users")

    def __init__(self, note=None):
        if not None == note and note != "":
            self.note = note

    def __str__(self):
        return str(f"user {self.user_id} was {self.mood.description} at {self.created_at}.")

    def __repr__(self):
        return str("UserMoodLog<id:", self.id) + f"{str(self.serialize())}>"

    # for sorting based on info here https://portingguide.readthedocs.io/en/latest/comparisons.html
    def __eq__(self, other):
        return self.created_at == other.created_at and self.user == other.user

    def __lt__(self, other):
        return self.created_at < other.created_at and self.user == other.user

    def serialize(self, userTimeZone=None,fmt='%Y-%m-%d %I:%M %p'):
        if not userTimeZone:
            userTimeZone = 'UTC' if self.user.timezone == None else self.user.timezone  
        tz=timezone(userTimeZone)
        local_datetime = self.created_at.astimezone(tz)
        formatted_date = local_datetime.strftime(fmt)
        response = {
            "user": f"{self.user}",
            "mood_description": f"{self.mood.description}",
            "note": f"{self.note}",
            "date": f"{formatted_date}",
        }

        return response


class Mood(db.Model):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    users = db.relationship(
        'UserMoodLog',
        cascade='all, delete',
        back_populates="mood"
    )

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return f"{self.description}"

    def __repr__(self):
        return f"id:{self.id}, description:{self.description}"

    def serialize(self):
        response = {
            "mood_id": f"{self.id}",
            "mood_description": f"{self.description}"
        }
        return response

    def update(self, description):
        self.description = description
        db.session.commit()


class User(UserMixin,  db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.Text, nullable=False)
    timezone = 'US/Eastern'
    moods = db.relationship(
        'UserMoodLog',
        cascade='all, delete-orphan',
        back_populates="user"
    )

    def __init__(self, email, password):
        self.email = email
        self.password = pwd_context.hash(password)

    def __repr__(self):
        return str(f"User<id:{self.id}, email:{self.email}>")

    def __str__(self):
        return str(self.email)

    def __eq__(self, other):
        return self.email == other.email and self.id == other.id

    def serialize(self):
        response = {
            "user_id": f"{self.id}",
            "user_email": f"{self.email}",
            "mood": f'{"" if not self.moods else sorted(self.moods)[-1].serialize()}'
        }
        return response

    def get_moods(self):
        return [mood.serialize() for mood in sorted(self.moods)]

    def get_simple_moods(self):
        result = [ {"mood":str(i.mood),"time":i.created_at} for i in self.moods ]

        return result
    
    def get_localized_log(self):
        result = [ i.serialize() for i in self.moods ]

        return result


    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def verify_password(self, passwrd_given):
        result = pwd_context.verify_and_update(str(passwrd_given), self.password)
        return result[0] # result is a tuple, first item is boolean

    def login(self, password):
        if self.verify_password(password):
            self._is_active = True
            self._is_authenticated = True
            self._is_anonymous = False

        else:
            self._is_authenticated = False
            self._is_active = False

    def logout(self):
        pass


# user loader for the Flask-Login module


@login_manager.user_loader
def load_user(user_id):
    result = None
    try:
        found_user = db.session.execute(select(User).where(User.email == user_id)).scalars().first()
    except:
        found_user = None
    result = found_user
    return result

