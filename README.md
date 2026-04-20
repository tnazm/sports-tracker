# sports-tracker

![Home page](https://github.com/tnazm/sports-tracker/blob/main/static/home%20page.png?raw=true)

![Weekly games view](https://github.com/tnazm/sports-tracker/blob/main/static/view%20of%20games%20weekly.png?raw=true)

## Features

* View weekly scores of games happening per week
* View scores of games played by your favorite teams
* Deployed on a Django/Gunicorn/nginx backend
* Dynamic Tailwind frontend webpage

### Mobile responsiveness

![Mobile responsiveness demo](https://github.com/tnazm/sports-tracker/blob/main/static/mobile%20responsitivity.png?raw=true)

### Track your favorite team's scores
Select favorite teams so that you can quickly glance at them in the
favorite team score display views.  Teams are saved and stored
uniquely per logged-in user.

![Updating a user's list of favorite teams](https://github.com/tnazm/sports-tracker/blob/main/static/favorite%20team%20updating%20view.png?raw=true)

![Viewing the scores of a user's favorite teams](https://github.com/tnazm/sports-tracker/blob/main/static/favorite%20team%20score%20display%20view.png?raw=true)

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
