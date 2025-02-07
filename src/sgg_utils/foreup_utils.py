import requests
import json
import logging
import os
from datetime import datetime, timedelta
from sgg_utils import cloud_utils
import time

API_URL = 'https://api.foreupsoftware.com/api_rest/index.php'

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def get_token(username, password):
    '''Get token from foreup api'''

    body =     {
        "email": username,
        "password": password
    }

    headers = {
    'Content-Type': 'application/json'
    }

    r = requests.post(f'{API_URL}/tokens', json=body, headers=headers)

    if r.status_code != 200:
        logging.error(f'Error: {r.status_code}')
        return None
    
    content = json.loads(r.content)
    token = content["data"]["id"]

    return token


def get_courses(token):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    r = requests.get(f'{API_URL}/courses', headers=headers)
    content = json.loads(r.content)
    
    courses = {}
    for i in range(len(content['data'])):
        courses[content['data'][i]['id']] = content['data'][i]['attributes']['title']

    return courses

def get_sale(token, course_id, sale_id, include=[]):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    if len(include) > 0:
        included = '?include=' + ','.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/sales/{sale_id}{included}', headers=headers)

    try:
        content = json.loads(r.content)
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')
        logging.error(f'Trying again...')
        time.sleep(5)
        r = requests.get(f'{API_URL}/courses/{course_id}/sales/{sale_id}{included}', headers=headers)
        logging.error(f'Retry status: {r.status_code}')
        content = json.loads(r.content)

    return content

def get_booking(token, course_id, teesheet_id, booking_id, include=[]):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    if len(include) > 0:
        included = '?include=' + ','.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/bookings/{booking_id}{included}', headers=headers)

    content = False
    iters = 0
    while content is False:
        try:
            content = json.loads(r.content)
        except json.JSONDecodeError:
            logging.error(f'Error: {r.status_code}')
            logging.error(f'Waiting 5 seconds...')
            time.sleep(5)
            r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/bookings/{booking_id}{included}', headers=headers)
            iters += 1
            if iters == 5:
                logging.error(f'Suspending attempts for this booking')
                return None
    return content

def get_teesheet(token, course_id, teesheet_id, include: list = []):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    if len(include) > 0:
        included = '?include=' + ','.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}{included}', headers=headers)

    try:
        content = r.json()
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')

    return content

def get_customer(token, course_id, customer_id, include=[]):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    if len(include) > 0:
        included = '?include=' + ','.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/customers/{customer_id}{included}', headers=headers)

    try:
        content = json.loads(r.content)
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')

    return content

def get_all_teesheets(token, course_id):
    '''get all teesheets for a course'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets', headers=headers)
    content = json.loads(r.content)
    return content


def get_hooks(token):
  '''Get all hooks from foreup api'''
  headers = {
      'Content-Type': 'application/json',
      'x-authorization': f'Bearer {token}'
  }
  r = requests.get(f'{API_URL}/hooks', headers=headers)
  content = json.loads(r.content)
  return content

def delete_hook(token, hook_id):
    '''Delete hook from foreup api'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.delete(f'https://api.foreupsoftware.com/api_rest/index.php/hooks/{hook_id}', headers=headers)
    return r.status_code

def create_hook(token, url, hook_type):
    '''Create hook in foreup api
    hook_type: string, teetime.updated or sale.created'''
    body = {
        "data": {
        "type": "api_hooks",
        "id": "1",
        "attributes": {
            "url": url,
            "event": hook_type
        }
        }
    }

    headers = {
    'Content-Type': 'application/json',
    'x-authorization': f'Bearer {token}'
    }

    r = requests.post('https://api.foreupsoftware.com/api_rest/index.php/hooks', json=body, headers=headers)
    content = json.loads(r.content)
    
    return content

def get_season(token, course_id, teesheet_id, season_id):
    '''get season for a course and teesheet'''

    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/seasons/{season_id}', headers=headers)
    content = json.loads(r.content)
    return content

def get_all_timeframes(token, course_id, teesheet_id, season_id):
    '''get timeframe for a season'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/seasons/{season_id}/timeframes', headers=headers)
    content = json.loads(r.content)
    return content

def get_timeframe(token, course_id, teesheet_id, season_id, timeframe_id):
    '''get timeframe for a season'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/seasons/{season_id}/timeframes/{timeframe_id}', headers=headers)
    content = json.loads(r.content)
    return content

def get_all_seasons(token, course_id, teesheet_id):
    '''get seasons for a course and teesheet'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/seasons', headers=headers)
    content = json.loads(r.content)
    return content

def get_seasons_dict(token, course_id, teesheet_id):
    '''get seasons for a course and teesheet'''
    seasons = get_all_seasons(token, course_id, teesheet_id)['data']
    season_dict = {}
    for season in seasons:
        season_dict[season['id']] = season['attributes']['name']
    return season_dict

def get_timeframe_dict(token, course_id, teesheet_id, season_id):
    '''get timeframes for a season'''
    timeframes = get_all_timeframes(token, course_id, teesheet_id, season_id)['data']
    timeframe_dict = {}
    for timeframe in timeframes:
        timeframe_dict[timeframe['id']] = timeframe['attributes']['name']
    return timeframe_dict


def get_pricing(token, course_id, teesheet_id, booking_id):
    '''get pricing for a season and timeframe'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/bookings/{booking_id}/pricing', headers=headers)
    content = json.loads(r.content)
    return content

def get_price_class(token, course_id, price_class_id):
    '''get price class for a season and timeframe'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/priceClasses/{price_class_id}', headers=headers)
    content = json.loads(r.content)
    return content

def get_all_price_classes(token, course_id):
    '''get price classes for a course'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/priceClasses', headers=headers)
    content = json.loads(r.content)
    return content

def get_bookings(token, course_id, teesheet_id, start_date, end_date = None, limit=100, include=[]):
    '''Accepts a course id, teesheet id and a start date.
    Returns an array of json data for a single day.
    If an end_date is provided, it will return all bookings between the start and end date.'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    if len(include) > 0:
        included = '&include=' + ','.join(include)
    else:
        included = ''

    sd = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date is None:
        ed = (sd + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        ed = end_date

    index = 0
    bookings_data = {'data': [], 'included': []}

    cont = True
    while cont:
        # Make a call to the API
        r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/bookings?limit={limit}&start={index}&startDate={sd}&endDate={ed}{included}', headers=headers)
        try:
            content = json.loads(r.content)
        except json.JSONDecodeError:
            print("Error: Invalid JSON response.")
            cont = False
            continue

        # Check that there is content
        if r.status_code == 200 and len(content['data']) > 0:
            bookings_data['data'].extend(content['data'])
            bookings_data['included'].extend(content['included'])

            ## end if results are less than limit, else increment the index
            if len(content['data']) < limit:
                print(f"No more results for {course_id}")
                break
            else:
                index += limit
        else:
            print("Final status code:", r.status_code)
            cont = False

    return bookings_data


def get_sales(token, course_id, start_date, end_date = None, limit=100, include=[]):
    '''Accepts a course id, teesheet id and a start date.
    Returns an array of json data for a single day.
    If an end_date is provided, it will return all bookings between the start and end date.'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    if len(include) > 0:
        included = '&include=' + ','.join(include)
    else:
        included = ''

    sd = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date is None:
        ed = (sd + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        ed = end_date

    index = 0
    sales_data = {'data': [], 'included': []}

    cont = True
    while cont:
        # Make a call to the API
        r = requests.get(f'{API_URL}/courses/{course_id}/sales?limit={limit}&start={index}&startDate={sd}&endDate={ed}{included}', headers=headers)
        try:
            content = json.loads(r.content)
        except json.JSONDecodeError:
            print("Error: Invalid JSON response.")
            cont = False
            continue

        # Check that there is content
        if r.status_code == 200 and len(content['data']) > 0:
            sales_data['data'].extend(content['data'])
            sales_data['included'].extend(content['included'])
            ## end if results are less than limit, else increment the index
            if len(content['data']) < limit:
                print(f"No more results for {course_id}")
                break
            else:
                index += limit
        else:
            print("Final status code:", r.status_code)
            cont = False

    return sales_data

def get_customers(token, course_id, limit = 100, testing=False):
    '''get customer from foreup api'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    start = 0
    cont = True
    customers = {'data': []}
    while cont:
        r = requests.get(f'{API_URL}/courses/{course_id}/customers?start={start}&limit={limit}', headers=headers)
        content = json.loads(r.content)

        if r.status_code == 200 and len(content['data']) > 0:
            customers['data'].extend(content['data'])
            if len(content['data']) < limit:
                cont = False
            else:
                start += limit
                print(f"Getting customers for {course_id} - {start} customers so far.")
        if testing:
            cont = False

    return customers

def get_items(token, course_id, include = [], limit = 100, testing=False):
    '''get customer from foreup api'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    start = 0
    cont = True


    if len(include) > 0:
        included = '&include=' + ','.join(include)
    else:
        included = ''
    
    items = {'data': []}
    while cont:
        r = requests.get(f'{API_URL}/courses/{course_id}/items?start={start}&limit={limit}{included}', headers=headers)
        content = json.loads(r.content)

        if r.status_code == 200 and len(content['data']) > 0:
            items['data'].extend(content['data'])
            if len(content['data']) < limit:
                cont = False
            else:
                start += limit
        if testing:
            cont = False

    return items

def get_item(token, course_id, item_id):
    '''get customer from foreup api'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    item = []
    r = requests.get(f'{API_URL}/courses/{course_id}/items/{item_id}', headers=headers)
    try:
        content = json.loads(r.content)
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')

    if r.status_code == 200 and len(content['data']) > 0:
        item.append(content['data'])

    return item

def get_special(token, course_id, teesheet_id, special_id):
    '''get special for a teesheet'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    url = f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/specials/{special_id}'
    r = requests.get(url, headers=headers)
    content = json.loads(r.content)
    return content

def get_specials(token, course_id, teesheet_id, testing=False):
    #trying this
    '''get specials from foreup api'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    url = f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/specials'
    r = requests.get(url, headers=headers)
    specials = json.loads(r.content)
    print(f"Specials retrieved: {len(specials)}")
    return specials


def get_stats(token, course_id, teesheet_id, start: str, end: str):
    '''get stats for a teesheet'''

    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/stats?start={start}&end={end}', headers=headers)

    try:
        content = json.loads(r.content)
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')
        return None
    
    return content

def get_hourly_stats(token, course_id, teesheet_id, date):
    '''get stats for a teesheet'''

    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    hours = ['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']

    hourly_dict = {}

    for hour in hours:
        r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/stats?start={date}T{hour}:00:00&end={date}T{hour}:59:59', headers=headers)
        try:
            content = json.loads(r.content)
        except json.JSONDecodeError:
            logging.error(f'Error: {r.status_code}')
            return None

        hourly_dict[hour] = content

    return hourly_dict


def get_teetime_slots(token, course_id, teesheet_id, date: str, start: str, end: str, params={}):
    '''
    Get teetimes for a course, teesheet, date, start time, and end time
    Accepts optional parameters:
    - bookingClassId
    - customerId
    - priceClassId
    - holes
    - scheduleSideId
    Example:
    params = {
        'bookingClassId': 1,
        'customerId': 9039,
        'priceClassId': 3,
        'holes': 'Both',
        'scheduleSideId': 4979
    }
    '''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    # Convert params dictionary to query string
    params_str = '&'.join([f'{k}={v}' for k, v in params.items()])

    # Construct the URL with or without params
    url = f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/teetimes?date={date}&startTime={start}&endTime={end}'
    if params_str:
        url += f'&{params_str}'

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        logging.error(f'Error: {r.status_code}')
        return None

    return r.json()

def get_terminals(token, course_id):
    '''get terminals from foreup api'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    url = f'{API_URL}/courses/{course_id}/terminals'
    r = requests.get(url, headers=headers)
    terminals = json.loads(r.content)
    return terminals