# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index


db = SQLAlchemy()


teachers_students = db.Table(
    'teachers_students',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey(
        'teachers.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey(
        'students.id'), primary_key=True),
    db.Column('grade', db.Integer, default=100),
    db.Column('class_name', db.String)    # adding multi_column uniqe contraint
    # found example here https://gist.github.com/asyd/3cff61ed09eabe187d3fbec2c8a3ee39
    # but it's for a class, to guessed on the syntax.
    # `flask db migrate` showed : Detected added unique constraint 'unique_class_teach_student' on '['class_name', 'teacher_id', 'student_id']'

    , db.UniqueConstraint('class_name', 'teacher_id', 'student_id', name='unique_class_teach_student')
)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    students = db.relationship(
        'Student', secondary=teachers_students,
        lazy='subquery',
        backref=db.backref('teachers', lazy=True),
        cascade='all, delete'
    )

    def __init__(self, name):
        self.name = name
        db.session.commit()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"id:{self.id}, name:{self.name}"

    def serialize(self):
        response = {
            "id": f"{self.id}",
            "name": f"{self.name}",
            "students": [student.name for student in self.students]
        }
        return response


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    # teachers = db.relationship(
    #     'Teacher', secondary=teachers_students,
    #     lazy='subquery',
    #     backref=db.backref('students', lazy=True)
    # )

    def __init__(self, name):
        self.name = name
        db.session.commit()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"id:{self.id}, name:{self.name}"

    def serialize(self):
        response = {
            "id": f"{self.id}",
            "name": f"{self.name}",
            "teachers": self.get_all_teachers()
        }
        return response

    def get_all_teachers(self):
        result = []
        for t in self.teachers:
            result.append(t.name)
        return result
