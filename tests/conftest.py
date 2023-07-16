"""
conftest base on documentation:
https://flask.palletsprojects.com/en/2.2.x/testing/


also referencing this post to create test database
https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2


"""

import pytest
from src import create_app
from src.models import db, User


@pytest.fixture()
def app():
    test_config = "../tests/testing_config.py"
    app = create_app(test_config)
    app.config.update({
        "TESTING": True,
        "SERVER_NAME": "localhost:5000",
        "SECRET_KEY": "Test-Only-Do-not-use-this",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "FLASK_ENV": "development"
    })

    # Initialize the database
    # db.init_app(app)
    with app.app_context():
        db.create_all()

        yield app

        # Teardown - Drop all database tables
        db.drop_all()


@pytest.fixture()
def testclient(app):
    return app.test_client()


@pytest.fixture()
def testclient_authenticated(testclient):
    username= 'test@example.com'
    password = 'password'
    db.session.add(User(username,password))
    db.session.commit()
    response = testclient.post('/auth/login',json={"username":username,"password":password,"remember_me":True,"submit":True, "csrf_token":"asyouwere"})
    return testclient

