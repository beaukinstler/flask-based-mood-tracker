"""
conftest base on documentation:
https://flask.palletsprojects.com/en/2.2.x/testing/


also referencing this post to create test database
https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2


"""

import pytest
from src import create_app
from src.models import db, User
from dotenv import load_dotenv
from flask_login import login_user, current_user, logout_user
from src.models import User

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv(dotenv_path=".env_test")


@pytest.fixture()
def app():

    app = create_app()
    # app.config.update({'SECRET_KEY':'testing'})

    # Initialize the database
    #db.init_app(app)
    with app.app_context():
        db.create_all()

        yield app
        db.session.close()
        # Teardown - Drop all database tables
        db.drop_all()


@pytest.fixture()
def testclient(app):
    return app.test_client()


@pytest.fixture()
def testclient_authenticated(app,testclient):
    # with app.app_context():
    # testclient = app.test_client()
    username= 'test@example.com'
    password = 'password'
    user = User(username,password)
    db.session.add(user)
    db.session.commit()
    with testclient:
        login_user(user, remember=True)
        
        yield testclient


