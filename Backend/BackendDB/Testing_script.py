import http.client
import json
from datetime import date,timedelta
from dotenv import load_dotenv
import os
import django
import sys
load_dotenv()
KEY=os.getenv("API_KEY")
KEY2=os.getenv("2ndAPI_KEY")
Today = date.today()
import time
## PATH TO BE ABLE TO ACCESS DJANGO MODELS
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportstracker.settings')
django.setup()
#import Hold ID mode to make sure we are not adding duplicate IDS
from sportstracker_app.models import HoldIDs, Game,GameData
## function to get all the game IDS for today and add them to the HoldIDs database (GameID, week, date)
Games=Game.objects.values_list("GameID",flat=True)
Gamedata=GameData.objects.values_list("GameID",flat=True)
Ids=HoldIDs.objects.values_list('GameID',flat=True)

def GameSummary(Gameid):
    conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v1.american-football.api-sports.io",
        'x-rapidapi-key': KEY2
        }

    conn.request("GET", f"/games/statistics/teams?id={Gameid}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    decoded =data.decode("utf-8")
    parsed = json.loads(decoded)

    return parsed

for game in Games:
    if game not in Gamedata:
        GameData.objects.create(GameID=game, data=GameSummary(game))
        time.sleep(6)
        print("Added data for game:",game)
    



# Game_Info = Get_Game_Info(17427)
# if Game_Info["game"]["status"]["long"]!="Finished" and  Game_Info["game"]["status"]["long"]!="Final/OT":
#   pass
# else:
#     gameid = id
#     week=  Game_Info["game"]["week"]
#     date = Game_Info["game"]["date"]["date"]
#     home_team=Game_Info["teams"]["home"]["name"] 
#     away_team=Game_Info["teams"]["away"]["name"]
#     home_score=Game_Info["scores"]["home"]["total"]
#     away_score=Game_Info["scores"]["away"]["total"]
#     Game.objects.create(GameID=gameid, HomeTeam=home_team, AwayTeam=away_team, HomeScore=home_score, AwayScore=away_score, Week=week, date=date)
#     print(f"{home_team} vs {away_team}    {week} added to database.")
