from flask import Blueprint, jsonify, abort, request
from ..models import Student, db, Teacher, teachers_students
from sqlalchemy.exc import IntegrityError

bp = Blueprint("students", __name__, url_prefix="/students")


@bp.route("", methods=['GET'])
def index():
    students = Student.query.all()
    result = []
    for student in students:
        result.append(student.serialize())
    return jsonify(result)


@bp.route("", methods=['POST'])
def create():
    if 'name' not in request.json:
        return abort(400)

    # name student
    student = Student(request.json['name'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.serialize())


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    student = Student.query.get_or_404(id)
    return jsonify(student.serialize())


@bp.route("/<int:id>/teacher", methods=['GET'])
def show_teacher(id: int):
    student = Student.query.get_or_404(id)
    return jsonify(student.teacher.serialize())


@bp.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    student = Student.query.get_or_404(id)
    result = {"message": "DELETE via HTTP",
              "id": student.id, 'student_name': student.name}
    db.session.delete(student)
    db.session.commit()
    return jsonify(result)


@bp.route("/<int:id>", methods=['PUT'])
def update(id: int):
    if 'name' not in request.json or 'teacher_id' not in request.json:
        return abort(400)
    student = Student.query.get_or_404(id)
    # name student
    name = request.json['name']
    teacher_id = request.json['teacher_id']

    if name is not None and name != '':
        student.name = name

    if teacher_id is not None and teacher_id != '':
        student.teacher_id = teacher_id

    db.session.commit()
    return jsonify(student.serialize())


@bp.route("/<int:id>/sign_up", methods=['POST'])
def sign_up(id: int):
    try:
        if 'teacher_id' not in request.json:
            return abort(400)
        teacher = Teacher.query.get_or_404(request.json['teacher_id'])
        student = Student.query.get_or_404(id)

        # lookup the id, but until then use default
        classname = "CS 101" if 'class' not in request.json else request.json['class']

        # student.teachers.append(teacher, class_name=classname)
        link = teachers_students.insert().values(
            student_id=student.id, teacher_id=teacher.id, class_name=classname)
        db.session.execute(link)

        db.session.commit()
        return jsonify(student.serialize())

    except IntegrityError as e:
        return abort(409)


@bp.route("/<int:id>/drop_class", methods=['DELETE'])
def drop_class(id: int):
    try:
        if 'teacher_id' not in request.json:
            return abort(400)
        teacher = Teacher.query.get_or_404(request.json['teacher_id'])
        student = Student.query.get_or_404(id)

        # lookup the id, but until then use default
        classname = "CS 101" if 'class' not in request.json else request.json['class']

        # student.teachers.append(teacher, class_name=classname)
        delete = (
            teachers_students.delete()
            .where(teachers_students.c.student_id == student.id)
            .where(teachers_students.c.teacher_id == teacher.id)
            .where(teachers_students.c.class_name == str(classname))
        )
        result = db.session.execute(delete)
        db.session.commit()

        return jsonify(student.serialize())

    except Exception() as e:

        return abort(400)
