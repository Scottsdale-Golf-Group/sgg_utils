import os
from sgg_utils import foreup_utils
from sgg_utils import cloud_utils
import json

SALE_TEST_CASE = {
    'COURSE_ID' : '21488',
    'SALE_ID' : '294869849',
    'SALE_TIME' : '2024-01-28T22:56:52+00:00'
}

BOOKING_TEST_CASE = {
    'COURSE_ID' : '21953',
    'TEESHEET_ID' : '9442',
    'BOOKING_ID' : 'TTID_102307410586cok',
    'DATE_BOOKED' : '2023-10-23T14:41:05+00:00',
    'SEASON_ID' : '80707',
    'TIMEFRAME_ID': '7680034',
}

BOOKING_TEST_CASE = {
    'COURSE_ID' : '21561',
    'TEESHEET_ID' : '8260',
    'BOOKING_ID' : 'TTID_0209183822o06u6',
    'DATE_BOOKED' : '2024-02-10T01:38:22+00:00',
    'SEASON_ID' : '103581',
    'TIMEFRAME_ID': '12758675',
    'PRICE_CLASS_ID': '36150',
}

JSON_LIST_EXAMPLE = [
    {
        "id": "1",
        "name": "John",
        "age": "21",
        "city": "New York"
    },
    {
        "id": "2",
        "name": "Danny",
        "age": "25",
        "city": "Los Angeles"
    },
    {
        "id": "3",
        "name": "Emma",
        "age": "28",
        "city": "Miami"
    }
]

def test_token():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    print(password[0])
    token = foreup_utils.get_token(username, password)
    assert token is not None

def test_courses():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    courses = foreup_utils.get_courses(token)
    assert courses is not None
    assert len(courses) > 0

def test_sale():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    sales = foreup_utils.get_sale(token, SALE_TEST_CASE['COURSE_ID'], SALE_TEST_CASE['SALE_ID'])
    assert sales[0]['attributes']['saleTime'] == SALE_TEST_CASE['SALE_TIME']

def test_booking():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    bookings = foreup_utils.get_booking(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['BOOKING_ID'], include=['players'])
    assert bookings[0]['attributes']['dateBooked'] == BOOKING_TEST_CASE['DATE_BOOKED']
    assert bookings[0]['course_id'] == BOOKING_TEST_CASE['COURSE_ID']

def test_teesheet():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    teesheets = foreup_utils.get_teesheet(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'])

    assert teesheets['data'] is not None
    assert teesheets['data']['type'] == 'teesheets'

def test_seasons():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    seasons = foreup_utils.get_all_seasons(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'])
    #print(seasons['data'][0])
    assert seasons['data'] is not None
    assert len(seasons['data']) > 0

# def test_seasons_dict():
#     username = os.environ.get('FOREUP_USER')
#     password = os.environ.get('FOREUP_PW')
#     token = foreup_utils.get_token(username, password)
#     seasons = foreup_utils.get_seasons_dict(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'])
#     print(seasons)
#     assert seasons is not None
#     assert len(seasons) > 0

# def test_season():
#     username = os.environ.get('FOREUP_USER')
#     password = os.environ.get('FOREUP_PW')
#     token = foreup_utils.get_token(username, password)
#     season = foreup_utils.get_season(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['SEASON_ID'])
#     print('Season:', season['data']['attributes']['name'])
#     assert season['data'] is not None
#     assert len(season) > 0

# def test_timeframes():
#     username = os.environ.get('FOREUP_USER')
#     password = os.environ.get('FOREUP_PW')
#     token = foreup_utils.get_token(username, password)
#     timeframes = foreup_utils.get_all_timeframes(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['SEASON_ID'])
#     courses = foreup_utils.get_courses(token)
#     # print(courses[BOOKING_TEST_CASE['COURSE_ID']])
#     # print(timeframes)
#     assert timeframes['data'] is not None
#     assert len(timeframes['data']) > 0

# def test_timeframe():
#     username = os.environ.get('FOREUP_USER')
#     password = os.environ.get('FOREUP_PW')
#     token = foreup_utils.get_token(username, password)
#     timeframes = foreup_utils.get_all_timeframes(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['SEASON_ID'])
#     timeframe_id = timeframes['data'][0]['id']
#     timeframes = foreup_utils.get_timeframe(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['SEASON_ID'], timeframe_id)
#     courses = foreup_utils.get_courses(token)
#     print(courses[BOOKING_TEST_CASE['COURSE_ID']])
#     print('Season:', BOOKING_TEST_CASE['SEASON_ID'])
#     print('Timeframe:', timeframes)
#     #print(timeframes)
#     assert timeframes['data'] is not None
#     assert len(timeframes['data']) > 0

# def test_timeframe_dict():
#     username = os.environ.get('FOREUP_USER')
#     password = os.environ.get('FOREUP_PW')
#     token = foreup_utils.get_token(username, password)
#     timeframes = foreup_utils.get_timeframe_dict(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['SEASON_ID'])
#     courses = foreup_utils.get_courses(token)
#     print(courses[BOOKING_TEST_CASE['COURSE_ID']])
#     print('Number of timeframes:', len(timeframes))
#     for key, value in timeframes.items():
#         print(f'Timeframe: {value} - ID: {key}')
#     assert timeframes is not None
#     assert len(timeframes) > 0

def test_pricing():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    pricing = foreup_utils.get_pricing(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], BOOKING_TEST_CASE['BOOKING_ID'])
    print(pricing)
    assert pricing['data'] is not None
    assert len(pricing) > 0

def test_price_class():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    price_class = foreup_utils.get_price_class(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['PRICE_CLASS_ID'])
    courses = foreup_utils.get_courses(token)
    print(courses[BOOKING_TEST_CASE['COURSE_ID']])
    print(price_class)
    assert price_class['data'] is not None
    assert len(price_class) > 0

# def test_backfill_bookings():
#     username = os.environ.get('FOREUP_USER')
#     password = os.environ.get('FOREUP_PW')
#     token = foreup_utils.get_token(username, password)
#     bookings = foreup_utils.get_bookings(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], sd='2023-07-30', ed='2023-07-31', include = ['players'], verbose=True)
    
#     assert bookings is not None
#     assert len(bookings) > 0
    
def test_day_bookings():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    bookings = foreup_utils.get_bookings(token, BOOKING_TEST_CASE['COURSE_ID'], BOOKING_TEST_CASE['TEESHEET_ID'], start_date='2023-01-18', include=['players'])
    assert len(bookings) == 104

def test_secret_manager():
    secret = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    assert secret is not None

def test_list_to_cloud_storage():
    response = cloud_utils.list_to_cloud_storage('sgg-test-bucket', JSON_LIST_EXAMPLE, 'test.json', timestamp=False)
    assert response == 'File test.json uploaded to sgg-test-bucket.'

def test_get_customers():
    username = 'mfutch78@gmail.com'
    password = cloud_utils.access_secret_version("593748364912", "FOREUP_MFUTCH", "latest")
    token = foreup_utils.get_token(username, password)
    customers = foreup_utils.get_customers(token, '21561', testing=True)
    assert customers[0]['type'] == 'customers'
    assert len(customers) > 0