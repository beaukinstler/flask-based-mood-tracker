from flask import Blueprint, jsonify, abort, request
from ..models import Mood
from sqlalchemy.exc import IntegrityError

bp = Blueprint("moods", __name__, url_prefix="/moods")


@bp.route("", methods=['GET'])
def index():
    moods = Mood.query.all()
    result = []
    for mood in moods:
        result.append(mood.serialize())
    return jsonify(result)


@bp.route("", methods=['POST'])
def create():
    if 'description' not in request.json:
        return abort(400)

    # name mood
    mood = Mood(request.json['name'])
    db.session.add(mood)
    db.session.commit()
    return jsonify(mood.serialize())


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    mood = Mood.query.get_or_404(id)
    return jsonify(mood.serialize())


@bp.route("/<int:id>/teacher", methods=['GET'])
def show_teacher(id: int):
    mood = Mood.query.get_or_404(id)
    return jsonify(mood.teacher.serialize())


@bp.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    mood = Mood.query.get_or_404(id)
    result = {"message": "DELETE via HTTP",
              "id": mood.id, 'mood_name': mood.name}
    db.session.delete(mood)
    db.session.commit()
    return jsonify(result)


@bp.route("/<int:id>", methods=['PUT'])
def update(id: int):
    if 'name' not in request.json or 'teacher_id' not in request.json:
        return abort(400)
    mood = Mood.query.get_or_404(id)
    # name mood
    name = request.json['name']
    teacher_id = request.json['teacher_id']

    if name is not None and name != '':
        mood.name = name

    if teacher_id is not None and teacher_id != '':
        mood.teacher_id = teacher_id

    db.session.commit()
    return jsonify(mood.serialize())


@bp.route("/<int:id>/sign_up", methods=['POST'])
def sign_up(id: int):
    try:
        if 'teacher_id' not in request.json:
            return abort(400)
        teacher = Teacher.query.get_or_404(request.json['teacher_id'])
        mood = Mood.query.get_or_404(id)

        # lookup the id, but until then use default
        classname = "CS 101" if 'class' not in request.json else request.json['class']

        # mood.teachers.append(teacher, class_name=classname)
        link = teachers_moods.insert().values(
            mood_id=mood.id, teacher_id=teacher.id, class_name=classname)
        db.session.execute(link)

        db.session.commit()
        return jsonify(mood.serialize())

    except IntegrityError as e:
        return abort(409)


@bp.route("/<int:id>/drop_class", methods=['DELETE'])
def drop_class(id: int):
    try:
        if 'teacher_id' not in request.json:
            return abort(400)
        teacher = Teacher.query.get_or_404(request.json['teacher_id'])
        mood = Mood.query.get_or_404(id)

        # lookup the id, but until then use default
        classname = "CS 101" if 'class' not in request.json else request.json['class']

        # mood.teachers.append(teacher, class_name=classname)
        delete = (
            teachers_moods.delete()
            .where(teachers_moods.c.mood_id == mood.id)
            .where(teachers_moods.c.teacher_id == teacher.id)
            .where(teachers_moods.c.class_name == str(classname))
        )
        result = db.session.execute(delete)
        db.session.commit()

        return jsonify(mood.serialize())

    except Exception() as e:

        return abort(400)
