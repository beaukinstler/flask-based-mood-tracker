import pytest
from flask import Flask
from src.models import db, Mood
import json


@pytest.mark.unit
def test_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient.get('/moods')
    assert response.status_code == 200


@pytest.mark.unit
def test_moods_post_create(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    data = {"description": "sad"}
    response = testclient.post('/moods', json=data)
    dict_data = json.loads(response.text)
    assert response.status_code == 200
    assert str(dict_data["id"]) == "1"
