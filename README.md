# sports-tracker

[[./static/home page.png]]

[[./static/view of games weekly.png]]

## Features

* View weekly scores of games happening per week
* View scores of games played by your favorite teams
* Deployed on a Django/Gunicorn/nginx backend
* Dynamic Tailwind frontend webpage

### Mobile responsiveness

[[./static/mobile responsitivity.png]]

### Track your favorite team's scores
Select favorite teams so that you can quickly glance at them in the
favorite team score display views.

[[./static/favorite team updating view.png]]

[[./static/favorite team score display view.png]]

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
