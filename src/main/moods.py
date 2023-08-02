from flask import Blueprint, jsonify, abort, url_for, flash
from flask import redirect as flask_redirect, request as flask_request, render_template as flask_render_template
from ..models import Mood, UserMoodLog, User
from sqlalchemy.exc import IntegrityError
from src import db
from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired
from flask_login import login_required, current_user
import requests
import json

bp = Blueprint("moods", __name__, url_prefix="/moods")


class MoodForm(FlaskForm):
    mood = HiddenField('mood', validators=[DataRequired()])


@bp.route("", methods=['GET', 'POST'])
@login_required
def index():
    form = MoodForm()

    if flask_request.method == 'POST':
        if form.validate():
            pass
        else:
            pass
        id = int(flask_request.form['button'])
        token = str(flask_request.form['token'])
        mood = Mood.query.all()
        moods = [m for m in mood if m.id == id]
        if moods:
            mood = moods[0]
            mood_description = mood.description
            response_data = {
                'message': f"Button {mood_description} pressed!",
                'token': f"{token}"
            }
            log = UserMoodLog()
            log.mood = mood
            current_user.moods.append(log)
            # db.session.add(log)
            db.session.commit()
            flash(f'Logged your {mood_description} mood...')
            return flask_redirect(url_for('users.me'))

    return flask_render_template('mood.html', form=form)


@bp.route("/all", methods=['GET'])
def all():
    headers = {"Accept": "application/json"}
    moods = requests.get(
        url_for('api_moods.index', _external=True), headers=headers, stream=False)
    if moods.status_code != 200:
        return abort(404)
    return flask_render_template('mood_list.html', moods=moods.json())



@bp.route("/create", methods=['POST'])
@login_required
def create():
    if 'description' not in flask_request.json:
        return abort(400)
    mood = Mood(flask_request.json['description'])
    try:
        db.session.add(mood)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        abort(409, description="Attempted Data Duplicate or other Integrity Error")
    return jsonify(mood.serialize())


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    mood = Mood.query.get_or_404(id)
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

    if 'description' not in flask_request.json:
        return abort(400)
    mood = Mood.query.get_or_404(id)

    description = flask_request.json['description']

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
