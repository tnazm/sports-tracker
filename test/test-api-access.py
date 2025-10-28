import http.client
import json
from datetime import datetime
Today=datetime.utcnow().date()
conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-rapidapi-host': "v1.american-football.api-sports.io",
    'x-rapidapi-key': "490fd3cc99aec2a51df1bda37df963a6"
    }

conn.request("GET", f"/games?league=1&date={Today}", headers=headers)

res = conn.getresponse()
data = res.read()

print(json.loads(data.decode("utf-8")))
