# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
# from sqlalchemy import Index
import datetime


db = SQLAlchemy()


class UserMoodLog(db.Model):
    """
    found example here https://gist.github.com/asyd/3cff61ed09eabe187d3fbec2c8a3ee39
    but it's for a class, to guessed on the syntax.
    """

    __tablename__ = 'users_moods'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id'), primary_key=False)
    mood_id = db.Column('mood_id', db.Integer, db.ForeignKey(
        'moods.id'), primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.utcnow)
    note = db.Column("notes", db.Text, nullable=True)
    user = db.relationship('User', back_populates="moods")
    mood = db.relationship('Mood', back_populates="users")

    def __init__(self, note):
        if not None == note and note != "":
            self.note = note

    # for sorting based on info here https://portingguide.readthedocs.io/en/latest/comparisons.html
    def __eq__(self, other):
        return self.created_at == other.created_at and self.user == other.user

    def __lt__(self, other):
        return self.created_at < other.created_at and self.user == other.user


class Mood(db.Model):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    users = db.relationship(
        'UserMoodLog',
        cascade='all, delete',
        back_populates="mood"
    )

    def __init__(self, description):
        self.description = description
        db.session.add(self)
        db.session.commit()

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


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    moods = db.relationship(
        'UserMoodLog',
        cascade='all, delete',
        back_populates="user"
    )

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.email == other.email and self.id == other.id

    def serialize(self):
        response = {
            "user_id": f"{self.id}",
            "user_email": f"{self.email}"
        }
        return response

    def get_moods(self):
        return [mood.serialize for mood in self.moods]


#####
# Examples of many to many
#####
# teachers_students = db.Table(
#     'teachers_students',
#     db.Column('id', db.Integer, primary_key=True, autoincrement=True),
#     db.Column('teacher_id', db.Integer, db.ForeignKey(
#         'teachers.id'), primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey(
#         'students.id'), primary_key=True),
#     db.Column('grade', db.Integer, default=100),
#     db.Column('class_name', db.String)    # adding multi_column uniqe contraint
#     # found example here https://gist.github.com/asyd/3cff61ed09eabe187d3fbec2c8a3ee39
#     # but it's for a class, to guessed on the syntax.
#     # `flask db migrate` showed : Detected added unique constraint 'unique_class_teach_student' on '['class_name', 'teacher_id', 'student_id']'

#     , db.UniqueConstraint('class_name', 'teacher_id', 'student_id', name='unique_class_teach_student')
# )


# class Teacher(db.Model):
#     __tablename__ = 'teachers'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, nullable=False)
#     students = db.relationship(
#         'Student', secondary=teachers_students,
#         lazy='subquery',
#         backref=db.backref('teachers', lazy=True),
#         cascade='all, delete'
#     )

#     def __init__(self, name):
#         self.name = name
#         db.session.commit()

#     def __str__(self):
#         return f"{self.name}"

#     def __repr__(self):
#         return f"id:{self.id}, name:{self.name}"

#     def serialize(self):
#         response = {
#             "id": f"{self.id}",
#             "name": f"{self.name}",
#             "students": [student.name for student in self.students]
#         }
#         return response


# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, nullable=False)

#     def __init__(self, name):
#         self.name = name
#         db.session.commit()

#     def __str__(self):
#         return f"{self.name}"

#     def __repr__(self):
#         return f"id:{self.id}, name:{self.name}"

#     def serialize(self):
#         response = {
#             "id": f"{self.id}",
#             "name": f"{self.name}",
#             "teachers": self.get_all_teachers()
#         }
#         return response

#     def get_all_teachers(self):
#         result = []
#         for t in self.teachers:
#             result.append(t.name)
#         return result
