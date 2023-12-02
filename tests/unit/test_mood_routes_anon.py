import pytest
from flask import Flask
from src.models import db, Mood
import json

### api tests

@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient.get('/api.v1/moods')

    assert response.status_code == 200


### api tests

@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    data = {"description":"happy"}
    response = testclient.post('/api.v1/moods/create',json=data)

    assert response.status_code == 302



@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_get_page(testclient):
    """
    GIVEN a Flask application nonauthenticated a mood in the database
    WHEN the '/api.v1/moods/1' page is altered with put/patch/delete
    THEN the response should be 302
    """

    """
    setup the database
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()


    # Create a test client using the Flask application configured for testing
    data = {"description":"happy"}
    

    response = testclient.put('/api.v1/moods/1',json=data)

    assert response.status_code == 302

    response = testclient.patch('/api.v1/moods/1',json=data)

    assert response.status_code == 302


    response = testclient.patch('/api.v1/moods/1',json=data)

    assert response.status_code == 302

