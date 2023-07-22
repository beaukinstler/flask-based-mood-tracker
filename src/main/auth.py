

from flask import Blueprint, jsonify, abort, url_for, flash
from flask import redirect as flask_redirect, request as flask_request, render_template as flask_render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from ..models import User
from src import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, logout_user
from werkzeug.urls import url_parse

bp = Blueprint("auth", __name__, url_prefix="/auth")


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
    if current_user.is_authenticated:
        next_page = url_for('users.index')
    form = LoginForm()
    # my valudate on submit isn't working. Added the POST check, at least for API
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.data['username']).scalar()
        if user is None:
            flash('Bad username or password.')
            return flask_redirect(url_for('auth.login'))
        user.login(form.data['password'])
        if user is None or not user.is_authenticated:
            flash('Bad username or password.')
            return flask_redirect(url_for('auth.login'))
        else:
            flash('Logged in successfully.')
            login_user(user, remember=True)
            # return flask_redirect(url_for('users.index'))

            # next_page = flask_request.args.get('next')
            next_page = url_for('main.index')
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for('users.index')

            return flask_redirect(next_page)
    return flask_render_template('login.html', form=form)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if flask_request.method == 'POST':
        username = flask_request.form['username']
        password = flask_request.form['password']
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
                return flask_redirect(url_for("auth.login"))

        flash(error)

    return flask_render_template('register.html')


@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        current_user.logout()
        logout_user()
        flash('Logged out successfully.')
        return flask_redirect(url_for('main.index'))
    else:
        flash("You aren't logged in")
        return flask_redirect(url_for('main.index'))
