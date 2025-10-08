import http.client
import json
from datetime import date
from dotenv import load_dotenv
import os
import django
import sys
load_dotenv()
KEY=os.getenv("API_KEY")
Today = date.today()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportstracker.settings')
django.setup()
from sportstracker_app.models import HoldIDs
def GamesToday():
    conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v1.american-football.api-sports.io",
        'x-rapidapi-key': KEY
        }

    conn.request("GET", f"/games?league=1&date={Today}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    live_games=data.decode("utf-8")
    parsed_live_games = json.loads(live_games) # make json readable

    for game in parsed_live_games["response"]:
        if not HoldIDs.objects.filter(GameID=game["game"]["id"]).exists():
            HoldIDs.objects.create(GameID=game["game"]["id"],week=game["game"]["week"],date =game["game"]["date"]["date"])
        ## ADDS GAME IDS TO DATABASE HAS TO BE RAN EVERYDAY



GamesToday()






