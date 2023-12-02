

from flask import Blueprint, jsonify, abort, url_for, flash
from flask import redirect as flask_redirect, request as flask_request, render_template as flask_render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from ..models import User
from src import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user
from werkzeug.urls import url_parse
from time import time

bp = Blueprint("api_auth", __name__, url_prefix="/api.v1/auth")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # see https://flask.palletsprojects.com/en/2.3.x/tutorial/views/ docs as well as
    # https://blog.pip.com/post/the-flask-mega-tutorial-part-v-user-logins/page/19
    # for my inspiration with all this

    # my valudate on submit isn't working. Added the POST check, at least for API
    if flask_request.method == 'POST':
        user = db.session.query(User).filter(
            User.email == flask_request.data['username']).scalar()
        if user is None:
            flash('Bad username or password.')
            return flask_redirect(url_for('auth.login'))
        user.login(form.data['password'])
        if user is None or not user.is_authenticated:
            flash('Bad username or password.')
            return flask_redirect(url_for('auth.login'))
        else:
            flash('Logged in successfully.')
            login_user(user)
            return flask_redirect(url_for('main.index'))

        next_page = flask_request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('users.index')

        return flask_redirect(next_page)
    return flask_render_template('login.html', form=form)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if flask_request.method == 'POST' and flask_request.content_type == 'application/json':
        username = flask_request.json.get("username")
        password = flask_request.json.get("password")
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                error = f"User {username} is already registered."
            else:
                return jsonify(new_user.serialize())
        

    # from here is an error response
    message = "Your registration didn't work. Ensure you send 'application/json' with 'username' and 'password'."
    flask_request.json.update({"message":message, "error":error})

    return jsonify(flask_request.json)


@bp.route('/logout')
def logout():
    message = {"user logged out":current_user,"datetime":time.now()}
    return jsonify(message)
