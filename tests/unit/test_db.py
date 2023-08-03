import pytest
from flask import Flask
from src.models import db, Mood


@pytest.fixture
def test_app():
    # Create a test Flask app instance
    app = Flask(__name__)
    app.config.from_mapping(
        TESTING=True,
        # Use an in-memory SQLite database for testing
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

        yield app

        # Teardown - Drop all database tables
        db.drop_all()


@pytest.fixture
def client(test_app):
    # Create a test client using the app fixture
    with test_app.test_client() as client:
        yield client


@pytest.mark.unit
def test_database(test_app):
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a Mood instance in the app context and commiting to datbase with "happy" as the data
    THEN the response of the query of the database will have that matching data in it's 'description'
    """

    with test_app.app_context():
        # Example: Insert a user into the database
        mood_data = 'happy'
        mood = Mood(mood_data)
        db.session.add(mood)
        db.session.commit()

        # Make assertions to verify the data insertion
        mood = Mood.query.get(1)
        assert mood.description == 'happy'

    # Roll back the changes to the database
    # with test_app.app_context():
    #     db.session.rollback()

    # Make assertions to verify the database rollback


@pytest.mark.unit
def test_model_update(test_app):
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a Mood instance in the app context and commiting to datbase with "happy" as the data
    THEN the response of the query of the database will have that matching data in it's 'description'
    """

    with test_app.app_context():
        # Example: Insert a user into the database
        mood_data = 'happy'
        mood = Mood(mood_data)
        db.session.add(mood)
        db.session.commit()

        # Make assertions to verify the data insertion
        mood = Mood.query.get(1)
        assert mood.description == 'happy'

        # use Model's update
        mood.update('sad')
        mood = Mood.query.get(1)
        assert mood.description == 'sad'

    # Make assertions to verify the database rollback



@pytest.mark.unit
def test_model_update(test_app):
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a Mood instance in the app context and commiting to datbase with "happy" as the data
    THEN the response of the query of the database will have that matching data in it's 'description'
    """

    with test_app.app_context():
        # Example: Insert a user into the database
        mood_data = 'happy'
        mood = Mood(mood_data)
        db.session.add(mood)
        db.session.commit()

        # Make assertions to verify the data insertion
        mood = Mood.query.get(1)
        assert mood.description == 'happy'

        # use Model's update
        mood.update('sad')
        mood = Mood.query.get(1)
        assert mood.description == 'sad'

