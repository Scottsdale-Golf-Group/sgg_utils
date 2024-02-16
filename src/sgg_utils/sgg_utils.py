import requests
import json
import logging
import os
import pandas as pd
from datetime import datetime, timedelta

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

def get_sale(token, course_id, sale_id, include: list = []):

    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }

    if len(include) > 0:
        included = '?include=' + '&'.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/sales/{sale_id}{included}', headers=headers)
    
    # Check if the response contains valid JSON
    try:
        content = r.json()
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')

    return content

def get_booking(token, course_id, teesheet_id, booking_id, include: list = []):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    if len(include) > 0:
        included = '?include=' + '&'.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/bookings/{booking_id}{included}', headers=headers)

    try:
        content = r.json()
    except json.JSONDecodeError:
        logging.error(f'Error: {r.status_code}')

    return content

def get_teesheet(token, course_id, teesheet_id, include: list = []):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    if len(include) > 0:
        included = '?include=' + '&'.join(include)
    else:
        included = ''

    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}{included}', headers=headers)

    try:
        content = r.json()
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

def get_bookings(token, course_id, teesheet_id, sd, ed, include: list = [], limit='100', verbose=False):
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    start = sd
    bookings_data = []

    if len(include) > 0:
        included = '?include=' + '&'.join(include)
    else:
        included = ''

    cont = True
    while cont:
        # Make a call to the API
        r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/bookings?limit={limit}&startDate={start}&endDate={ed}{included}', headers=headers)

        # Check if the response contains valid JSON
        try:
            content = r.json()
            
        except json.JSONDecodeError:
            print("Error: Invalid JSON response.")
            cont = False
            continue

        # Check that there is content
        if r.status_code == 200 and len(content['data']) > 0:
            bookings_data.extend(content['data'])

            # Update the new start date from last entry
            ts = content['data'][-1]['attributes']['dateBooked']
            datetime_obj = datetime.fromisoformat(ts) - timedelta(hours=0) + timedelta(seconds=1)
            start = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')
            if verbose:
                print("Rolling window", start)
        else:
            print("Final status code:", r.status_code)
            cont = False

    # Create DataFrames from the collected data
    bookings_df = pd.DataFrame(bookings_data)
    #players_df = pd.DataFrame(players) ## worry about players later
    bookings_df.columns = ['type', 'booking_id', 'attributes', 'relationships']

    # Clean up df
    bookings_df['attributes'] = bookings_df['attributes'].apply(lambda x: json.dumps(x))
    bookings_df['course_id'] = course_id
    bookings_df['teesheet_id'] = teesheet_id
    bookings_df['name_course'] = get_courses(token)[course_id]
    if len(include) > 0:
        bookings_df['relationships'] = bookings_df['relationships'].apply(lambda x: json.dumps(x))

    # clean up
    top_cols = ['booking_id', 'course_id', 'teesheet_id', 'name_course']
    cols = top_cols + [col for col in bookings_df.columns if col not in top_cols]
    bookings_df = pd.DataFrame(bookings_df[cols]) 

    return bookings_df




