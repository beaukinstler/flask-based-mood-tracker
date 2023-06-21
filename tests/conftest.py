"""
conftest base on documentation:
https://flask.palletsprojects.com/en/2.2.x/testing/


also referencing this post to create test database
https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2


"""

import pytest
from src import create_app


@pytest.fixture()
def app():
    test_config = ".\\tests\\testing_config.py"
    app = create_app(test_config)
    app.config.update({
        "TESTING": True,
        'SERVER_NAME': 'localhost:5000'
    })

    # other setup can go here
    app.testing = True
    yield app

    # clean up / reset resources here


@pytest.fixture()
def testclient(app):

    with app.test_client() as client:
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
