from flask import Blueprint, jsonify, abort, request
from ..models import User
from sqlalchemy.exc import IntegrityError
from src import db
from flask_login import login_required
from sqlalchemy import select


bp = Blueprint("api_users", __name__, url_prefix="/api.v1/users")


@bp.route("", methods=['GET'])
@login_required
def index():
    users = db.session.execute(select(User).order_by(User.id)).scalars().all()
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


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


@bp.route("/delete", methods=['DELETE'])
def delete():
    if 'username' not in request.json:
        return abort(400)

    user = db.session.scalar(select(User).where(User.email == request.json['username']).limit(1))
    if not user.verify_password(request.json['password']):
        return abort(400)
    result = {"message": "DELETE via HTTP",
              "id": user.id, 'email': user.email}
    db.session.delete(user)
    db.session.commit()
    return jsonify(result)


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
