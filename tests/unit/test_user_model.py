import pytest
from flask import Flask
from src.models import db, User
from sqlalchemy.exc import IntegrityError


@pytest.mark.users
@pytest.mark.unit
def test_model_update(testclient):
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

    # Make assertions to verify the data insertion
    user_from_db = User.query.get(1)
    assert user_from_db.id == 1


@pytest.mark.users
@pytest.mark.unit
def test_model_update(testclient):
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a User instance in the app context and commiting to datbase with email and password
    THEN the new user object will have and id property == 1
    """

    # Example: Insert a user into the database
    user_email = 'user01@example.com'
    user_password = 'password'
    user = User(email=user_email, password=user_password)
    db.session.add(user)
    db.session.commit()
    assert user.id == 2

    with pytest.raises(IntegrityError):
        user2 = User(email=user_email, password=user_password)
        db.session.add(user2)
        db.session.commit()
    db.session.rollback()

    user_email = 'nondup@example.com'

    user2 = User(email=user_email, password=user_password)
    db.session.add(user2)
    db.session.commit()
    assert user2.id == 3


@pytest.mark.admin
@pytest.mark.users
@pytest.mark.unit
def test_first_user_is_admin(testclient):
    """
    GIVEN a new user
    WHEN first created
    THEN then user.is_admin returns "False"
    """

    # Example: Insert a user into the database
    user = db.session.query(User).first()
    assert user.is_admin == True
