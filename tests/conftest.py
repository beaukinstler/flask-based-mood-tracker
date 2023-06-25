"""
conftest base on documentation:
https://flask.palletsprojects.com/en/2.2.x/testing/


also referencing this post to create test database
https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2


"""

import pytest
from src import create_app
from src.models import db


@pytest.fixture()
def app():
    test_config = "..\\tests\\testing_config.py"
    app = create_app(test_config)
    app.config.update({
        "TESTING": True,
        'SERVER_NAME': 'localhost:5000'
    })

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

        yield app

        # Teardown - Drop all database tables
        db.drop_all()


@pytest.fixture()
def testclient(app):
    return app.test_client()
    # with app.test_client() as client:
    #     yield
