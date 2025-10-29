import http.client
import json
from datetime import date,timedelta
from dotenv import load_dotenv,find_dotenv
import os
import sys
import requests
import time

load_dotenv(find_dotenv())
KEY=os.getenv("API_KEY")
print(KEY)

def request(endpoint, params):
    if not KEY:
        raise Exception("No API key supplied.  Please set the environment variable API_KEY before using.")
    url = "https://v1.american-football.api-sports.io"
    headers = {
        'x-rapidapi-host': "v1.american-football.api-sports.io",
        'x-rapidapi-key': KEY
    }

    max_retries = 2
    RETRY_DELAY_443 = 60
    RETRY_DELAY = 1

    for attempt in range(max_retries):
        try:
            r = requests.get(url + "/" + endpoint, params=params, headers=headers, timeout=1)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1:
                retryDelay = RETRY_DELAY_443 if e.args[0].status_code == 443 else RETRY_DELAY
                print(f"Request failed: {e}.  Retrying in {retryDelay} seconds..")
                time.sleep(retryDelay)
            else:
                print(f"Max retries reached.  Final error: {e}")

    return r.json()

# def request(getreq):
#     if not KEY:
#         raise Exception("No API key supplied.  Please set the environment variable API_KEY before using.")

#     conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

#     headers = {
#         'x-rapidapi-host': "v1.american-football.api-sports.io",
#         'x-rapidapi-key': KEY
#         }

#     conn.request("GET", getreq, headers=headers)

#     res = conn.getresponse()
#     data = res.read()

#     decoded = data.decode("utf-8")
#     parsed = json.loads(decoded)

#     return dict(parsed)

def getGame(gameID):
    """Request API for a specific game.  Returns JSON data response."""
    return request("games", {"id": gameID})

def getTeam(teamID):
    """Request API for a specific team.  Returns JSON data response."""
    return request("teams", {"id": teamID})

def validateGame(parsed):
    parsed = dict(parsed)
    response = parsed['response']
    if not parsed['response'] or parsed['errors']:
        return False
    if response['game']['stage'] != 'Regular Season':
        return False
    if response['league']['id'] != 1 and response['league']['season'] != 2025:
        return False

    return True
