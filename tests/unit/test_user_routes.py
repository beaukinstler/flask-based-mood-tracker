import pytest
from flask import Flask
from src.models import db, User, load_user
import json


@pytest.mark.users
@pytest.mark.unit
def test_users_load_user_login_manager(testclient):
    user = User('test@example.com', 'password')
    db.session.add(user)
    db.session.commit()
    loaded_user = load_user(1)



@pytest.mark.users
@pytest.mark.unit
def test_users_get_page_no_users(testclient):
    """
    given: a GET to url /users

    when: when the user is authorized to access that url but there are no users in the database

    then: get a response with status 200

    """
    response = testclient.get('/users')
    assert response.status_code == 302

    """
    given: a GET to url /users

    when: when the user is authorized to access that url but and there are users in the database

    then: get a response with status 200

    """
    response = testclient.get('/users')
    assert response.status_code == 302

    """
    given: a GET to url /users

    when: when the user is authorized to access that url and there is at least 1 user in the database

    then: get a response with all the user ids and their mood totals

    """
    assert response.text.find("user_id") < 0

@pytest.mark.auth
@pytest.mark.users
@pytest.mark.unit
def test_users_get_page_with_users(testclient):
    """
    given: a GET to url /users

    when: when the user is authorized to access that url but and there are users in the database

    then: get a response with status 200

    """
    username= 'test@example.com'
    password = 'password'
    db.session.add(User(username,password))
    db.session.commit()
    response = testclient.post('/auth/login',json={"username":username,"password":password})
    response = testclient.get('/users')
    assert response.status_code == 200

    """
    given: a GET to url /users

    when: when the user is authorized to access that url and there is at least 1 user in the database

    then: get a response with all the user ids and their mood totals

    """
    assert response.text.find("user_id") > 0
    response_dict = json.loads(response.text)
    assert str(response_dict[0]["user_id"]) == "1"

@pytest.mark.users
@pytest.mark.unit
def test_users_get_page_not_authorized(testclient):
    """
    given: a GET to url /users

    when: when the user is authorized to access that url but and there are users in the database

    then: get a response with status 200

    """
    response = testclient.get('/users')
    assert response.status_code == 302




    """
    given: a post to url /users/create

    when: with body {'email':<valid email format>, ‘password’:”some string”

    then: a new user is added to the the database and the response includes a user ID
    """



    """
    given: a post to url /users/create

    when: with body {'email':not valid, ‘password’:”some string”

    then: 404 
    """


    """
    given: a post to url /users/create

    when: with body {} or missing

    then: 404
    """