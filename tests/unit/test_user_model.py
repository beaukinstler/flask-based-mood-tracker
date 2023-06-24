import pytest
from flask import Flask
from src.models import db, Mood
import json

@pytest.mark.users
@pytest.mark.unit
def test_users_get_page(testclient):
    """
    given: a GET to url /users

    when: when the user is authorized to access that url

    then: get a response with status 200

    """
    response = testclient.get('/users')
    assert response.status_code == 200

    """
    given: a GET to url /users

    when: when the user is authorized to access that url

    then: get a response with all the user ids and their mood totals

    """
    assert response.text.contains("user_id") == False



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