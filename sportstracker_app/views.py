import sys
from pathlib import Path
from django.conf import settings
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import http.client, os
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from sportstracker_app.models import GameData
from .models import Game
from .forms import CustomUserCreationForm

load_dotenv()
KEY = os.getenv("API_KEY")

BACKEND_PATH = Path(settings.BASE_DIR) / "Backend" / "BackendDB"
BACKEND_PATH_STR = str(BACKEND_PATH.resolve())
if BACKEND_PATH_STR not in sys.path:
    sys.path.insert(0, BACKEND_PATH_STR)

Weeks = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]

nfl_teams = [
    "Arizona Cardinals",
    "Atlanta Falcons",
    "Baltimore Ravens",
    "Buffalo Bills",
    "Carolina Panthers",
    "Chicago Bears",
    "Cincinnati Bengals",
    "Cleveland Browns",
    "Dallas Cowboys",
    "Denver Broncos",
    "Detroit Lions",
    "Green Bay Packers",
    "Houston Texans",
    "Indianapolis Colts",
    "Jacksonville Jaguars",
    "Kansas City Chiefs",
    "Las Vegas Raiders",
    "Los Angeles Chargers",
    "Los Angeles Rams",
    "Miami Dolphins",
    "Minnesota Vikings",
    "New England Patriots",
    "New Orleans Saints",
    "New York Giants",
    "New York Jets",
    "Philadelphia Eagles",
    "Pittsburgh Steelers",
    "San Francisco 49ers",
    "Seattle Seahawks",
    "Tampa Bay Buccaneers",
    "Tennessee Titans",
    "Washington Commanders"
]

TEAM_ABBR = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS"
}

def pick_team(request):
    teams_ctx = [{"name": n, "abbr": TEAM_ABBR[n]} for n in nfl_teams]
    return render(request, "newuserhub.html", {"Weeks": Weeks, "Teams": teams_ctx})

def home(request):
    Games = Game.objects.all()
    context = {"Games": Games, "Weeks": Weeks}
    return render(request, 'main.html', context)

def week(request, num):
    Games = Game.objects.filter(Week=f"Week {num}")
    return render(request, 'week.html', {"Games": Games, "week_number": num, "Weeks": Weeks})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Welcome to Half-Time, your account has been created")
            return render(request, "register.html", {'form': form})
        else:
            currenterrors = dict(form.errors)
            errors = []
            for errornames in currenterrors.values():
                for error in errornames:
                    errors.append(error)
            messages.error(request, "Error")
            return render(request, "register.html", {'form': form, "Weeks": Weeks, "errors": errors})
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {'form': form, "Weeks": Weeks})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'The username or password (or both) is invaild. Please enter the correct credentials.')
            return redirect('login')
    return render(request, "login.html", {"Weeks": Weeks})

def logout_view(request):
    logout(request)
    return redirect("home")

def GameSummary(Gameid):
    if not GameData.objects.filter(GameID=Gameid).exists():
        Gameid = str(Gameid)
        conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
        headers = {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': KEY
        }
        conn.request("GET", f"/games/statistics/teams?id={Gameid}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        decoded = data.decode("utf-8")
        parsed = json.loads(decoded)
        if parsed["results"] == 0:
            return "CANT add game"
        GameData.objects.create(GameID=Gameid, data=parsed)
        return {
            "HomeTeam": parsed["response"][0],
            "AwayTeam": parsed["response"][1]
        }
    else:
        data = GameData.objects.get(GameID=Gameid).data
        return {
            "HomeTeam": data["response"][0],
            "AwayTeam": data["response"][1]
        }

def load_game_summary(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        game_id = data.get("game_id")
        if not game_id:
            return JsonResponse({"error": "Missing game_id"}, status=400)
        try:
            summary = GameSummary(game_id)
            return JsonResponse(summary if isinstance(summary, dict) else {"error": summary}, status=200 if isinstance(summary, dict) else 400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)
