import http.client
import json
from dotenv import load_dotenv
import os
load_dotenv()
KEY=os.getenv("API_KEY")

def Get_Game_Info(Gameid):
    conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v1.american-football.api-sports.io",
        'x-rapidapi-key': KEY
        }

    conn.request("GET", f"/games/statistics/teams?id={Gameid}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    decoded =data.decode("utf-8")
    parsed = json.loads(decoded)

    return parsed
## GO TO DATABASE ???

