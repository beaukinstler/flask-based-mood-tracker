
import os,json
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

migrate = Migrate()
bootstrap = Bootstrap5()


def page_not_found(e):
  return render_template('403.html'), 403

def create_app():
    config_file = "config.py"
    if os.environ.get('FLASK_ENV') == 'development':
        config_file = "test_config.py"
    config_file = "../" + config_file

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile(config_file, silent=True)

    app.register_error_handler(403, page_not_found)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # initialize login managers with app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


#######
# importing and registering the bluprints from the api folder
#######


    from .api import moods as api_moods, users as api_users, auth as api_auth
    from .main import main, users, moods, auth
    app.register_blueprint(moods.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(api_moods.bp)
    app.register_blueprint(api_users.bp)
    app.register_blueprint(api_auth.bp)
    app.register_blueprint(main)

    if os.environ.get('FLASK_ENV') == 'development':
        with app.app_context():
            db.create_all()

    return app
