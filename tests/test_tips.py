import pytest


def test_tips(testclient):

    response = testclient.get()
    assert response is not None
