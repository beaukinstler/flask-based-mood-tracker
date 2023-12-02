from flask import Blueprint, jsonify, abort, request
from ..models import Mood
from sqlalchemy.exc import IntegrityError
from src import db
from flask_login import login_required, current_user

bp = Blueprint("api_moods", __name__, url_prefix="/api.v1/moods")


@bp.route("", methods=['GET'])
def index():
    moods = Mood.query.all()
    result = [mood.serialize() for mood in moods]
    if result is None:
        return jsonify({"message": "No Data"}), 404
    return jsonify(result)


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    mood = Mood.query.get_or_404(id)
    return jsonify(mood.serialize())


"""
Authentication required routes 
"""


@bp.route("/create", methods=['POST'])
@login_required
def create():
    if 'description' not in request.json:
        return abort(400)
    mood = Mood(request.json['description'])
    try:
        db.session.add(mood)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        abort(409, description="Attempted Data Duplicate or other Integrity Error")
    return jsonify(mood.serialize())


@bp.route("/<int:id>", methods=['DELETE'])
@login_required
def delete(id: int):
    mood = Mood.query.get_or_404(id)
    result = {"message": "DELETE via HTTP",
              "id": mood.id, 'description': mood.description}
    db.session.delete(mood)
    db.session.commit()
    return jsonify(result)


@bp.route("/<int:id>", methods=['PUT', 'PATCH'])
@login_required
def update(id: int):
    """
    update a mood name
    """

    if 'description' not in request.json:
        return abort(400)
    mood = Mood.query.get_or_404(id)

    description = request.json['description']

    if description is not None and description != '':
        mood.description = description

    db.session.commit()
    return jsonify(mood.serialize())


# @bp.route("/<int:id>/sign_up", methods=['POST'])
# def sign_up(id: int):
#     try:
#         if 'teacher_id' not in request.json:
#             return abort(400)
#         teacher = Teacher.query.get_or_404(request.json['teacher_id'])
#         mood = Mood.query.get_or_404(id)

#         # lookup the id, but until then use default
#         classname = "CS 101" if 'class' not in request.json else request.json['class']

#         # mood.teachers.append(teacher, class_name=classname)
#         link = teachers_moods.insert().values(
#             mood_id=mood.id, teacher_id=teacher.id, class_name=classname)
#         db.session.execute(link)

#         db.session.commit()
#         return jsonify(mood.serialize())

#     except IntegrityError as e:
#         return abort(409)


# @bp.route("/<int:id>/drop_class", methods=['DELETE'])
# def drop_class(id: int):
#     try:
#         if 'teacher_id' not in request.json:
#             return abort(400)
#         teacher = Teacher.query.get_or_404(request.json['teacher_id'])
#         mood = Mood.query.get_or_404(id)

#         # lookup the id, but until then use default
#         classname = "CS 101" if 'class' not in request.json else request.json['class']

#         # mood.teachers.append(teacher, class_name=classname)
#         delete = (
#             teachers_moods.delete()
#             .where(teachers_moods.c.mood_id == mood.id)
#             .where(teachers_moods.c.teacher_id == teacher.id)
#             .where(teachers_moods.c.class_name == str(classname))
#         )
#         result = db.session.execute(delete)
#         db.session.commit()

#         return jsonify(mood.serialize())

#     except Exception() as e:

#         return abort(400)
