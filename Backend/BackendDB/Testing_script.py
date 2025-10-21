import http.client
import json
from datetime import date,timedelta
from dotenv import load_dotenv
import os
import django
import sys
load_dotenv()
KEY=os.getenv("API_KEY")
Today = date.today()
import time
## PATH TO BE ABLE TO ACCESS DJANGO MODELS
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportstracker.settings')
django.setup()
#import Hold ID mode to make sure we are not adding duplicate IDS
from sportstracker_app.models import HoldIDs, Game
## function to get all the game IDS for today and add them to the HoldIDs database (GameID, week, date)
Games=Game.objects.values_list("GameID",flat=True)

Ids=HoldIDs.objects.values_list('GameID',flat=True)


for game in Games:
    if game not in Ids:
        print(game)

