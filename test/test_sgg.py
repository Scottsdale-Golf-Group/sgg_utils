import os
from sgg_utils import sgg_utils

SALE_TEST_CASE = {
    'COURSE_ID' : '21488',
    'SALE_ID' : '294869849',
    'SALE_TIME' : '2024-01-28T22:56:52+00:00'
}

BOOKING_TEST_CASE = {
    'COURSE_ID' : '21953',
    'TEESHEET_ID' : '9442',
    'BOOKING_ID' : 'TTID_102307410586cok',
    'DATE_BOOKED' : '2023-10-23T14:41:05+00:00'
}

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

def test_sale():
    username = os.environ.get('FOREUP_USER')
    password = os.environ.get('FOREUP_PW')
    token = sgg_utils.get_token(username, password)
    sales = sgg_utils.get_sale(token, SALE_TEST_CASE['COURSE_ID'], SALE_TEST_CASE['SALE_ID'])
    assert sales['data']['attributes']['saleTime'] == SALE_TEST_CASE['SALE_TIME']

def test_booking():
    username = os.environ.get('FOREUP_USER')
    password = os.environ.get('FOREUP_PW')
    token = sgg_utils.get_token(username, password)
    bookings = sgg_utils.get_booking(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['BOOKING_ID'])
    assert bookings['data']['attributes']['dateBooked'] == BOOKING_TEST_CASE['DATE_BOOKED']

def test_teesheet():
    username = os.environ.get('FOREUP_USER')
    password = os.environ.get('FOREUP_PW')
    token = sgg_utils.get_token(username, password)
    teesheets = sgg_utils.get_teesheet(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'])
    assert teesheets['data'] is not None
    assert len(teesheets) > 0

def test_season():
    username = os.environ.get('FOREUP_USER')
    password = os.environ.get('FOREUP_PW')
    token = sgg_utils.get_token(username, password)
    seasons = sgg_utils.get_season(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'])
    assert seasons['data'] is not None
    assert len(seasons) > 0