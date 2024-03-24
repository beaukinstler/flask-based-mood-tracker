import pytest
from flask import Flask
from src.models import db, User
import json
import requests
from flask import url_for

@pytest.mark.gui
@pytest.mark.unit
@pytest.mark.moods
def test_users_all_page(testclient_authenticated_many_users):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/users/all' page is requested (GET)
    THEN check that the response is valid
    """
    with testclient_authenticated_many_users as test_client:


        gui = test_client.get(url_for('users.all_users'), follow_redirects=True)
        assert gui.status_code == 200

        # Check that the page contains the user's name
        assert b'test_user1' or b'test1' in gui.data
        assert b'test_user2' or b'test2' in gui.data
        assert b'<a href="/users/all?page=2&amp;per_page=10"> 2 </a>' in gui.data

