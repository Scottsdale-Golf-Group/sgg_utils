import requests
import json
import logging
import os

API_URL = 'https://api.foreupsoftware.com/api_rest/index.php'

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def get_token(username, password):
    '''Get token from foreup api'''
    logging.info(API_URL)

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

    print(f'{API_URL}/courses/{course_id}/sales/{sale_id}{include}') 
    r = requests.get(f'{API_URL}/courses/{course_id}/sales/{sale_id}{included}', headers=headers)
    
    # Check if the response contains valid JSON
    try:
        content = r.json()
    except json.JSONDecodeError:
        print("Error: Invalid JSON response.")

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
        print("Error: Invalid JSON response.")

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
        print("Error: Invalid JSON response.")

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


def get_season(token, course_id, teesheet_id):
    '''get season for a course and teesheet'''

    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/seasons', headers=headers)
    content = json.loads(r.content)
    return content

def get_season_timeframe(token, course_id, teesheet_id, season_id):
    '''get timeframe for a season'''
    headers = {
        'Content-Type': 'application/json',
        'x-authorization': f'Bearer {token}'
    }
    r = requests.get(f'{API_URL}/courses/{course_id}/teesheets/{teesheet_id}/seasons/{season_id}/timeframes', headers=headers)
    content = json.loads(r.content)
    return content