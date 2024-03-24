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

    user_email = 'userxyz@example.com'
    user_password = 'password'
    result_of_query_before = User.query.filter_by(email=user_email).first()
    assert result_of_query_before == None
    user = User(email=user_email, password=user_password)    
    db.session.add(user)
    db.session.commit()
    result_of_query_after = User.query.filter_by(email=user_email).first()

    assert result_of_query_after.email == "userxyz@example.com"

    with pytest.raises(IntegrityError):
        user2 = User(email=user_email, password=user_password)
        db.session.add(user2)
        db.session.commit()
    db.session.rollback()

    user_email = 'nondup@example.com'

    user2 = User(email=user_email, password=user_password)
    db.session.add(user2)
    db.session.commit()
    new_user = User.query.filter_by(email=user_email).first()

    assert new_user.email == user_email


@pytest.mark.admin
@pytest.mark.users
@pytest.mark.unit
def test_first_user_is_admin(testclient_authenticated_many_users):
    """
    GIVEN a new user
    WHEN first created
    THEN then user.is_admin returns "False"
    """

    # Example: Insert a user into the database
    user = db.session.query(User).first()
    assert user.is_admin == True

    user2 = db.session.query(User).get(2)
    assert user2.is_admin == False

@pytest.mark.admin
@pytest.mark.users
@pytest.mark.unit
def test_first_of_many_user_is_admin(testclient_authenticated_many_users):
    """
    GIVEN a new user
    WHEN first created
    THEN then user.is_admin returns "False"
    """

    # Example: Insert a user into the database
    user = db.session.query(User).first()
    assert user.is_admin == True

