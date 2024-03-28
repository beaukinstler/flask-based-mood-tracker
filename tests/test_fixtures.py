import pytest


def test_fixture_testclient(testclient):
    response = testclient.get()
    assert response is not None


def test_fixture_testclient_authenticated(testclient_authenticated):

    response = testclient_authenticated.get()
    assert response is not None

def test_fixture_testclient_authenticated(testclient_authenticated_many_users):

    response = testclient_authenticated_many_users.get()
    assert response is not None