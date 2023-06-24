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

    assert user.is_authenticated == False
    assert user.is_active == False
    assert user.is_anonymous == False
    assert user.get_id() == '0'


@pytest.mark.auth
@pytest.mark.users
@pytest.mark.unit
def test_flask_login_properties_database_committed(testclient):
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a User instance in the app context and commiting to datbase with email and password
    THEN the new user object will have and id property == 1
    """

    # Example: Insert a user into the database
    user_email = 'user@example.com'
    user_password = 'password'
    user = User(email=user_email, password=user_password)

    db.session.add(user)
    db.session.commit()

    assert user.is_authenticated == False
    assert user.is_active == False
    assert user.is_anonymous == False
    assert user.get_id() == '1'

    user.is_authenticated = True
    db.session.commit()
    users = db.session.query(User).all()

    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].is_authenticated == True
