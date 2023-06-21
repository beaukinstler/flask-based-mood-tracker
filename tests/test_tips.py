import pytest


def test_tips(testclient):

    response, status = testclient.get()
    assert response is not None
