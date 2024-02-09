import os
from sgg_utils import sgg_utils

def test_token():
    username = os.environ.get('FOREUP_USER')
    password = os.environ.get('FOREUP_PW')
    token = sgg_utils.get_token(username, password)
    assert token is not None

def test_courses():
    username = os.environ.get('FOREUP_USER')
    password = os.environ.get('FOREUP_PW')
    token = sgg_utils.get_token(username, password)
    courses = sgg_utils.get_courses(token)
    assert courses is not None
    assert len(courses) > 0
    