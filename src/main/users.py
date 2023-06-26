from flask import Blueprint, jsonify, abort, request
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


@bp.route("/all", methods=['GET'])
@login_required
def all_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result)


# @bp.route("", methods=['POST'])
# def create():
#     if 'description' not in request.json:
#         return abort(400)
#     user = User(request.json['description'])
#     return jsonify(user.serialize())


# @bp.route("/<int:id>", methods=['GET'])
# def show(id: int):
#     user = User.query.get_or_404(id)
#     return jsonify(user.serialize())


# @bp.route("/<int:id>", methods=['DELETE'])
# def delete(id: int):
#     user = User.query.get_or_404(id)
#     result = {"message": "DELETE via HTTP",
#               "id": user.id, 'description': user.description}
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify(result)


# @bp.route("/<int:id>", methods=['PUT', 'PATCH'])
# def update(id: int):
#     """
#     update a user name
#     """

#     if 'description' not in request.json:
#         return abort(400)
#     user = User.query.get_or_404(id)

#     description = request.json['description']
#     teacher_id = request.json['teacher_id']

#     if description is not None and description != '':
#         user.description = description

#     db.session.commit()
#     return jsonify(user.serialize())
