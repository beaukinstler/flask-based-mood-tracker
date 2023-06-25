from src.main import main
from flask import render_template, redirect, url_for


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html", title='Home Page')


@main.route('/login')
def login():
    return redirect(url_for("auth.login"))
