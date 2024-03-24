from flask import Blueprint, jsonify, request as flask_request, render_template, abort, redirect, url_for
from ..models import User
from src import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user



bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=['GET'])
@login_required
def index():
    result = current_user.serialize()
    return jsonify(result)

@bp.route("/me", methods=['GET'])
@login_required
def me():
    serialized = current_user.serialize()
    moods = current_user.get_localized_log()
    moods.reverse()
    return render_template('me.html', user_data=serialized, moods=moods)


@bp.route("/all", methods=['GET'])
@login_required
def all_users():
    if current_user.is_admin:
        current_page = flask_request.args.get('page', type=int, default=1)
        per_page = flask_request.args.get('per_page',  type=int, default=10)
        pages = User.query.paginate(current_page, per_page, False)
        return render_template('all_users.html', pages=pages, current_user=current_user)
        
    else:
        return abort(403, "Not authorized to view all users")

@bp.route("/<int:user_id>/edit", methods=['GET','POST'])
@login_required
def update_user(user_id: int):
    if current_user.is_admin:
        if flask_request.method == 'GET':
            user = User.query.get_or_404(user_id)
            return render_template('user.html', user=user, current_user=current_user)
        elif flask_request.method == 'POST':
            user = User.query.get_or_404(user_id)
            user.is_admin = True if flask_request.form.get('is_admin', False) == 'on' else False
            user.email = flask_request.form['email']
            db.session.commit()
            return redirect(url_for('users.all_users'))
    else:
        return abort(403, "Not authorized to edit users")
