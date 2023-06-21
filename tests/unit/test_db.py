import pytest
from flask import Flask
from src.models import db, Mood


@pytest.fixture
def app():
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
def client(app):
    # Create a test client using the app fixture
    with app.test_client() as client:
        yield client

@pytest.mark.unit
def test_database(app, client):
    # Insert test data into the database
    # You can customize this based on your models and data structure
    with app.app_context():
        # Example: Insert a user into the database
        mood_data = 'happy'
        mood = Mood(mood_data)
        db.session.add(mood)
        db.session.commit()

        # Make assertions to verify the data insertion
        mood = Mood.query.get(1)
        assert mood.description == 'happy'

    # Roll back the changes to the database
    with app.app_context():
        db.session.rollback()

    # Make assertions to verify the database rollback
