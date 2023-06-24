import pytest
from flask import Flask
from src.models import db, User
import flask_login


@pytest.mark.auth
@pytest.mark.users
@pytest.mark.unit
def test_flask_login_properties():
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a User instance in the app context and commiting to datbase with email and password
    THEN the new user object will have and id property == 1
    """

    # Example: Insert a user into the database
    user_email = 'user@example.com'
    user_password = 'password'
    user = User(email=user_email, password=user_password)

    assert user.is_authenticated is not None
    assert user.is_active is not None
    assert user.is_anonymous == False
    assert user.get_id() == 0
