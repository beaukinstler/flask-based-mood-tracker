from flask import Blueprint, jsonify, abort, request
from ..models import Teacher, db, Student, teachers_students
from sqlalchemy.exc import IntegrityError

bp = Blueprint("teachers", __name__, url_prefix="/teachers")


@bp.route("", methods=['GET'])
def index():
    teachers = Teacher.query.all()
    result = []
    for teacher in teachers:
        result.append(teacher.serialize())
    return jsonify(result)


@bp.route("", methods=['POST'])
def create():
    try:
        if 'name' not in request.json:
            return abort(400)

        # name teacher
        teacher = Teacher(request.json['name'])
        db.session.add(teacher)
        db.session.commit()
        return jsonify(teacher.serialize())
    except IntegrityError as e:
        return jsonify({"message": "Error creating teacher. Make sure a unique name is being used."})


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    teacher = Teacher.query.get_or_404(id)
    return jsonify(teacher.serialize())


@bp.route("/<int:id>/students", methods=['GET'])
def show_students(id: int):
    teacher = Teacher.query.get_or_404(id)
    return jsonify([student.name for student in teacher.students])


@bp.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    teacher = Teacher.query.get_or_404(id)
    result = {"message": "DELETE via HTTP",
              "id": teacher.id, 'teacher_name': teacher.name}
    db.session.query(teachers_students).filter(
        teachers_students.c.teacher_id == teacher.id).update({'teacher_id': 3})
    db.session.commit()
    db.session.delete(teacher)
    db.session.commit()
    return jsonify(result)


@bp.route("/<int:id>", methods=['PUT'])
def update(id: int):
    if 'new_teacher_id' not in request.json:
        return abort(400)
    new_teacher_id = request.json['new_teacher_id']
    old_teacher = Teacher.query.get_or_404(id)
    students = old_teacher.students

    new_teacher = Teacher.query.get_or_404(new_teacher_id)
    # TODO what will this do about the class names? did the arrive with the students link?
    new_teacher.students.extend(students)
    # old_teacher.students = []

    db.session.commit()
    return jsonify(new_teacher.serialize())
