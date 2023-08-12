from sqlalchemy import select, delete, insert, update
from flask import Blueprint, jsonify, abort, url_for, flash
from flask import redirect as flask_redirect, request as flask_request, render_template as flask_render_template
from ..models import Mood, UserMoodLog, User
from sqlalchemy.exc import IntegrityError
from src import db
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length
from flask_login import login_required, current_user
import requests
import json

bp = Blueprint("moods", __name__, url_prefix="/moods")


class MoodForm(FlaskForm):
    note = TextAreaField('note', validators=[Length(min=0, max=240)], render_kw={'placeholder': '[Optional] Leave a note...'})
    happy = SubmitField('Happy',id=5, render_kw={'class': 'btn btn-primary'}, )
    sad = SubmitField('Sad',id=2, render_kw={'class': 'btn btn-warning'})



@bp.route("", methods=['GET', 'POST'])
@login_required
def index():
    form = MoodForm()

    if flask_request.method == 'POST':
        if form.validate():
            pass
        else:
            flash('Invalid Form')
            return flask_redirect(url_for('moods.index'))
        moods = db.session.execute(select(Mood).order_by(Mood.id.asc())).scalars().all()
        mood_name = [ field for field in flask_request.form if field in [ m.description for m in moods] ].pop()
        mood = [ mood for mood in moods if mood.description in flask_request.form  ].pop()

        if mood:
            # mood_description = mood.description
            log = UserMoodLog()
            log.mood = mood
            log.user = current_user
            log.note = form.note.data
            db.session.add(log)
            try:
                db.session.commit()
                flash(f'Logged your {mood.description} mood...')
            except Exception as e:
                db.session.rollback()
                print(e)
                if str(e).find('check_last_record_time') > 0:
                    flash(f"You recently logged a mood. It's too soon to log your {mood.description} mood...")
                else:
                    flash(f'There was a problem logging your {mood.description} mood...')
        return flask_redirect(url_for('users.me'))
    return flask_render_template('mood.html', form=form)





@bp.route("/all", methods=['GET'])
def all():

    moods = db.session.execute(select(Mood).order_by(Mood.id.asc())).scalars().all()
    if moods is None:
        return abort(404)
    return flask_render_template('mood_list.html', moods=moods)



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
