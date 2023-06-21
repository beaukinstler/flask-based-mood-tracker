import pytest
from flask import Flask
from src.models import db, Mood





@pytest.mark.unit
def test_hotest_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """


    # Create a test client using the Flask application configured for testing
    
    response = testclient.get('/moods')
    assert response.status_code == 200

