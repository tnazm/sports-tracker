
import http.client
import json
from dotenv import load_dotenv
import os
load_dotenv()
KEY=os.getenv("API_KEY")


## JUST A FUNCTION TO GET BASIC INFO FROM A GAME ID
def GameSummary(Gameid):
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

    return (
        
        {"HomeTeam":parsed["response"][0],
         
         
         "AwayTeam":parsed["response"][1]
         
         
        }
         )


        ## sends json data back
