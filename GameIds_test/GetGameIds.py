import http.client
import json
from datetime import date
Today = date.today()
from dotenv import load_dotenv
import os
load_dotenv()
KEY=os.getenv("API_KEY")

NFL_Gamesid=[] # array to hold (Game ID)
# funciton that gets all NFL games today
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

        NFL_Gamesid.append(game["game"]["id"])
        ## add the game id to the array

GamesToday()
## drop the array of games today into the Live_games file
with open("Games_This_Week", "r") as f: ## Write TO DATABASE????, ##WOULD BE CLEARED EVERY WEEK
    games=json.load(f)
## reading array from file then adding all the games today to that array
for game in NFL_Gamesid:
    if game not in games:
        games.append(game)

with open("Games_This_Week", "w") as f:
    json.dump(games, f, indent=4)