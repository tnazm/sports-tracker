# sports-tracker

## Features

* View scores of games happening per week
* TODO View scores of games played by your favorite teams
* Django/gunicorn/nginx backend
* Tailwind frontend

## Installation
Obtain an API key for [[https://api-sports.io]].  Replace the stock
value in [[./env.template]] and rename it as ```.env```.

Running locally (for test purposes):

``` shell
git clone https://github.com/tnazm/sports-tracker
pip install -r requirements.txt
python3 manage.py runserver
```

Deployment:

``` shell
git clone https://github.com/tnazm/sports-tracker
pip install -r requirements.txt
chmod +x ./start_server.sh
./start_server.sh
./
```
