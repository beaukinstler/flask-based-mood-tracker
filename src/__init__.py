
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

test_config = None


def create_app(test_config=None):
    if os.environ.get('FLASK_ENV') == 'development':
        test_config = "../tests/testing_config.py"
    app = Flask(__name__, instance_relative_config=True)
    # commenting the below out to read form a config.py file, instead

    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/oos_game',
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     SQLALCHEMY_ECHO=True
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('../config.py', silent=True)
        app.config["SECRET_KEY"] = "sdlfkajwdkj90234uofdkvnv0e89h9028"
        app.config["WTF_CSRF_SECRET_KEY"] = "sdlfkajwdkj90234uofdkvnv0e89h9028"
    else:
        # load the test config if passed in
        # app.config.from_mapping(test_config)
        app.config.from_pyfile(test_config, silent=True)
        app.config["SECRET_KEY"] = "sdlfkajwdkj90234uofdkvnv0e89h9028"
        app.config["WTF_CSRF_SECRET_KEY"] = "sdlfkajwdkj90234uofdkvnv0e89h9028"

    db.init_app(app)
    migrate = Migrate(app, db)

    # initialize login managers with app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


#######
# Example of importing and registering the bluprints from the api folder
#######
    # from .api import teachers, students
    # app.register_blueprint(teachers.bp)
    # app.register_blueprint(students.bp)

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
