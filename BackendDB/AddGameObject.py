import os
import django
import sys
import json


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportstracker.settings')
django.setup()

## CREATE GAME OBJECTS IN DATABASE
from sportstracker_app.models import Game, HoldIDs
from BackendDB.GetGameJson import Get_Game_Info
ids = HoldIDs.objects.all().values_list('GameID')
list(ids)
for id in ids:
    if not Game.objects.filter(GameID=id).exists():
        gameid = id[0]
        week=id[1]
        date = id[2]
        Game_Info = Get_Game_Info(id[0])
        home_team=Game_Info["teams"]["home"]["name"] 
        away_team=Game_Info["teams"]["away"]["name"]
        home_score=Game_Info["scores"]["home"]["total"]
        away_score=Game_Info["scores"]["away"]["total"]
        Game.objects.create(GameID=gameid, HomeTeam=home_team, AwayTeam=away_team, HomeScore=home_score, AwayScore=away_score, Week=week, date=date)

print("Games added successfully!")
