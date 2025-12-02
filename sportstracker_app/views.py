import sys
from pathlib import Path
from django.conf import settings
import json
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import http.client, os
from dotenv import load_dotenv
from sportstracker_app.models import GameData, Profile, Game, Team
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse

load_dotenv()
KEY = os.getenv("API_KEY")

BACKEND_PATH = Path(settings.BASE_DIR) / "Backend" / "BackendDB"
BACKEND_PATH_STR = str(BACKEND_PATH.resolve())

if BACKEND_PATH_STR not in sys.path:
    sys.path.insert(0, BACKEND_PATH_STR)

from .forms import CustomUserCreationForm, ProfileForm

Weeks = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]

nfl_teams = [
    "Arizona Cardinals","Atlanta Falcons","Baltimore Ravens","Buffalo Bills",
    "Carolina Panthers","Chicago Bears","Cincinnati Bengals","Cleveland Browns",
    "Dallas Cowboys","Denver Broncos","Detroit Lions","Green Bay Packers",
    "Houston Texans","Indianapolis Colts","Jacksonville Jaguars","Kansas City Chiefs",
    "Las Vegas Raiders","Los Angeles Chargers","Los Angeles Rams","Miami Dolphins",
    "Minnesota Vikings","New England Patriots","New Orleans Saints","New York Giants",
    "New York Jets","Philadelphia Eagles","Pittsburgh Steelers","San Francisco 49ers",
    "Seattle Seahawks","Tampa Bay Buccaneers","Tennessee Titans","Washington Commanders"
]

def home(request):
    Games = Game.objects.all()
    last_saved_week = request.session.get('saved_week', 1)

    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
        team = fav_teams[0] if fav_teams else 1
    else:
        team = None

    context = {"Games": Games, "Weeks": Weeks, "saved": last_saved_week, "Team": team}
    return render(request, 'main.html', context)

def week(request, num):
    Games = Game.objects.filter(Week=f"Week {num}")
    request.session['saved_week'] = num 

    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
        team = fav_teams[0] if fav_teams else 1
    else:
        team = None

    return render(request, 'week.html', {"Games": Games, "week_number": num, "Weeks": Weeks, "Team": team})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Welcome to Half-Time, your account has been created")
            return render(request, "register.html", {'form': form})
        else:
            currenterrors = dict(form.errors)
            errors = [err for val in currenterrors.values() for err in val]
            messages.error(request, "Error")
            return render(request, "register.html", {'form': form, "Weeks": Weeks, "errors": errors})
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {'form': form, "Weeks": Weeks})

def pick_team(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team.get("fav_teams", [])
        team = fav_teams[0] if fav_teams else 1
    else:
        team = None

    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        user_favteam = current_user.favorite_team.get("fav_teams", [])
        favorites = request.session.get('favorite_teams', user_favteam)

        if request.method == 'POST':
            selected_team = request.POST.get('team')
            action = request.POST.get('action')

            if selected_team:
                if action == 'add' and selected_team not in favorites:
                    favorites.append(selected_team)
                elif action == 'remove' and selected_team in favorites:
                    favorites.remove(selected_team)

            request.session['favorite_teams'] = favorites
            return redirect('pickteam')

        Profile.objects.filter(user=current_user.user).update(favorite_team={"fav_teams": favorites})

        return render(request, "newuserhub.html", {
            "Weeks": Weeks, "Teams": nfl_teams, "Favorites": favorites,
            "currentuser": current_user, "Team": team
        })

    return render(request, "newuserhub.html", {"Weeks": Weeks, "Teams": nfl_teams})

def user_account(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
        team = fav_teams[0] if fav_teams else 1
    else:
        team = None

    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        return render(request, 'account.html', {
            'user': current_user.user,
            'favorites': current_user.favorite_team.get("fav_teams", []),
            'Weeks': Weeks,
            'Team': team,
            'profile': current_user,
            'profile_form': ProfileForm(instance=current_user),
        })

    return render(request, 'account.html', {"Weeks": Weeks, "Team": team})

@login_required
def update_account(request):
    if request.method == 'POST':
        prof = Profile.objects.get(user=request.user.id)
        form = ProfileForm(request.POST, instance=prof)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
        else:
            messages.error(request, 'There was a problem saving your profile.')

    return redirect('account')

@login_required
def delete_account(request):
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'DELETE':
            user = request.user
            logout(request)
            try:
                user.delete()
            except Exception:
                messages.error(request, 'Unable to delete account.')
                return redirect('account')

            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
        else:
            messages.error(request, 'Please confirm account deletion.')
    return redirect('account')

def fav_team_games(request, team):
    current_user = Profile.objects.get(user=request.user.id)
    fav_teams = current_user.favorite_team["fav_teams"]
    Games = Game.objects.filter(Q(HomeTeam=team) | Q(AwayTeam=team))

    return render(request, "favteamgames.html", {
        "Games": Games, "Weeks": Weeks, "Favs": fav_teams,
        "Current_Team": team, "Team": team
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user=request.user.id)
            login_count = current_user.login_count

            Profile.objects.filter(user=current_user.user).update(login_count=login_count + 1)

            if login_count == 0:
                return redirect("pickteam")
            return redirect("home")

        messages.error(request, 'Invalid username or password.')
        return redirect('login')

    return render(request, "login.html", {"Weeks": Weeks})

def logout_view(request):
    logout(request)
    return redirect("home")

def GameSummary(Gameid):
    if not GameData.objects.filter(GameID=Gameid).exists():
        conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
        headers = {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': KEY
        }

        conn.request("GET", f"/games/statistics/teams?id={Gameid}", headers=headers)
        res = conn.getresponse()
        data = res.read()

        parsed = json.loads(data.decode("utf-8"))
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
            return JsonResponse(summary)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

from collections import defaultdict

def standings_view(request):
    from collections import defaultdict

    # For navbar favorite-team logic
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
        team = fav_teams[0] if fav_teams else 1
    else:
        team = None

    games = Game.objects.exclude(HomeScore=0, AwayScore=0)

    # Full team → (conference, division)
    divisions = {
        "Buffalo Bills":               ("AFC", "East"),
        "Miami Dolphins":              ("AFC", "East"),
        "New England Patriots":        ("AFC", "East"),
        "New York Jets":               ("AFC", "East"),

        "Baltimore Ravens":            ("AFC", "North"),
        "Cincinnati Bengals":          ("AFC", "North"),
        "Cleveland Browns":            ("AFC", "North"),
        "Pittsburgh Steelers":         ("AFC", "North"),

        "Houston Texans":              ("AFC", "South"),
        "Indianapolis Colts":          ("AFC", "South"),
        "Jacksonville Jaguars":        ("AFC", "South"),
        "Tennessee Titans":            ("AFC", "South"),

        "Denver Broncos":              ("AFC", "West"),
        "Kansas City Chiefs":          ("AFC", "West"),
        "Las Vegas Raiders":           ("AFC", "West"),
        "Los Angeles Chargers":        ("AFC", "West"),

        "Dallas Cowboys":              ("NFC", "East"),
        "New York Giants":             ("NFC", "East"),
        "Philadelphia Eagles":         ("NFC", "East"),
        "Washington Commanders":       ("NFC", "East"),

        "Chicago Bears":               ("NFC", "North"),
        "Detroit Lions":               ("NFC", "North"),
        "Green Bay Packers":           ("NFC", "North"),
        "Minnesota Vikings":           ("NFC", "North"),

        "Atlanta Falcons":             ("NFC", "South"),
        "Carolina Panthers":           ("NFC", "South"),
        "New Orleans Saints":          ("NFC", "South"),
        "Tampa Bay Buccaneers":        ("NFC", "South"),

        "Arizona Cardinals":           ("NFC", "West"),
        "Los Angeles Rams":            ("NFC", "West"),
        "San Francisco 49ers":         ("NFC", "West"),
        "Seattle Seahawks":            ("NFC", "West"),
    }

    # Full team → logo abbr (file name stem)
    logo_abbr = {
        "Buffalo Bills": "BUF",
        "Miami Dolphins": "MIA",
        "New England Patriots": "NE",
        "New York Jets": "NYJ",

        "Baltimore Ravens": "BAL",
        "Cincinnati Bengals": "CIN",
        "Cleveland Browns": "CLE",
        "Pittsburgh Steelers": "PIT",

        "Houston Texans": "HOU",
        "Indianapolis Colts": "IND",
        "Jacksonville Jaguars": "JAX",
        "Tennessee Titans": "TEN",

        "Denver Broncos": "DEN",
        "Kansas City Chiefs": "KC",
        "Las Vegas Raiders": "LV",
        "Los Angeles Chargers": "LAC",

        "Dallas Cowboys": "DAL",
        "New York Giants": "NYG",
        "Philadelphia Eagles": "PHI",
        "Washington Commanders": "WAS",

        "Chicago Bears": "CHI",
        "Detroit Lions": "DET",
        "Green Bay Packers": "GB",
        "Minnesota Vikings": "MIN",

        "Atlanta Falcons": "ATL",
        "Carolina Panthers": "CAR",
        "New Orleans Saints": "NO",
        "Tampa Bay Buccaneers": "TB",

        "Arizona Cardinals": "ARI",
        "Los Angeles Rams": "LAR",
        "San Francisco 49ers": "SF",
        "Seattle Seahawks": "SEA",
    }

    # Aggregate stats by team
    stats = defaultdict(lambda: {
        "name": "",
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "games": 0,
        "pct": 0.0,
        "conference": "",
        "division": "",
        "logo": "",
    })

    for g in games:
        home = g.HomeTeam
        away = g.AwayTeam
        hs = g.HomeScore
        as_ = g.AwayScore

        for name in [home, away]:
            if stats[name]["name"] == "":
                stats[name]["name"] = name
                conf, div = divisions.get(name, ("", ""))
                stats[name]["conference"] = conf
                stats[name]["division"] = div
                abbr = logo_abbr.get(name)
                if abbr:
                    stats[name]["logo"] = f"sportstracker_app/img/nfl/{abbr}.svg"

        if hs > as_:
            stats[home]["wins"] += 1
            stats[away]["losses"] += 1
        elif as_ > hs:
            stats[away]["wins"] += 1
            stats[home]["losses"] += 1
        else:
            stats[home]["ties"] += 1
            stats[away]["ties"] += 1

    # conferences → divisions → teams
    standings_by_conf = {
        "AFC": {"East": [], "North": [], "South": [], "West": []},
        "NFC": {"East": [], "North": [], "South": [], "West": []},
    }

    for name, s in stats.items():
        s["games"] = s["wins"] + s["losses"] + s["ties"]
        s["pct"] = s["wins"] / s["games"] if s["games"] > 0 else 0.0
        conf = s["conference"]
        div = s["division"]
        if conf in standings_by_conf and div in standings_by_conf[conf]:
            standings_by_conf[conf][div].append(s)

    for conf in standings_by_conf:
        for div in standings_by_conf[conf]:
            standings_by_conf[conf][div].sort(
                key=lambda x: (-x["pct"], -x["wins"], x["name"])
            )

    conference_labels = {
        "AFC": "American Football Conference",
        "NFC": "National Football Conference",
    }
    division_order = ["East", "North", "South", "West"]

    conferences = []
    for conf_key in ["AFC", "NFC"]:
        conf_obj = {
            "key": conf_key,
            "name": conference_labels[conf_key],
            "divisions": [],
        }
        for div in division_order:
            conf_obj["divisions"].append({
                "name": div,
                "teams": standings_by_conf[conf_key][div],
            })
        conferences.append(conf_obj)

    context = {
        "conferences": conferences,
        "Weeks": Weeks,
        "Team": team,
    }
    return render(request, "standings.html", context)
