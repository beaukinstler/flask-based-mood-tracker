import pytest
from flask import Flask
from src.models import db, User
from flask_login import logout_user, login_user, current_user


class TestUserAuth:
    """
    Test the User model with authentication

    """

    @pytest.mark.auth
    @pytest.mark.users
    @pytest.mark.unit
    def test_user_login_password(self, testclient):
        """
        GIVEN a User model
        WHEN setting the password as 'password'
        THEN the verify_password function should succeed, and the actual password will be a hashed string
        """

        # Example: Insert a user into the database
        user_email = 'user@example.com'
        user_password = 'password'
        user = User(email=user_email, password=user_password)
        assert user.password != 'password'
        assert user.verify_password('password')
        assert len(user.password) > 100
        # pre_db_password = user.password

        db.session.add(user)
        db.session.commit()
        user_from_db = User.query.filter(User.email==user_email).first()
        assert user_from_db.verify_password('password')


    @pytest.mark.auth
    @pytest.mark.users
    @pytest.mark.unit
    def test_flask_login_properties(self, testclient):
        """
        GIVEN a Flask application configured for in this test file for testing via a fixture
        WHEN creating a User instance in the app context and commiting to datbase with email and password
        THEN the new user object will have and id property == 1
        """

        # Example: Insert a user into the database
        with testclient.application.app_context():
            user_email = 'user@example.com'
            user_password = 'password'
            user = User(email=user_email, password=user_password)

            assert user.is_authenticated == True
            assert user.is_active == True
            assert user.is_anonymous == False
            # for the flask_login, i think they want the username
            assert user.get_id() == 'user@example.com'




    @pytest.mark.auth
    @pytest.mark.users
    @pytest.mark.unit
    def test_flask_login_properties_database_committed(self, testclient):
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
        user = User.query.filter_by(email='user@example.com').first()
        user.login(user_password)
        login_user(user)
        assert current_user.is_authenticated == True
        assert current_user.email == 'user@example.com'



    @pytest.mark.auth
    @pytest.mark.users
    @pytest.mark.unit
    def test_flask_login_logout_user(self, testclient):
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
        user = User.query.filter_by(email='user@example.com').first()
        user.login(user_password)
        login_user(user)
        logout_user()
        assert current_user.is_authenticated == False

