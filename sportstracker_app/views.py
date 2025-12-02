import sys
from pathlib import Path
from django.conf import settings
import json
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import http.client,os
from dotenv import load_dotenv
from sportstracker_app.models import GameData,Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
load_dotenv()
KEY = os.getenv("API_KEY")

BACKEND_PATH = Path(settings.BASE_DIR) / "Backend" / "BackendDB"
BACKEND_PATH_STR = str(BACKEND_PATH.resolve())

if BACKEND_PATH_STR not in sys.path:
    sys.path.insert(0, BACKEND_PATH_STR)

from django.shortcuts import render, redirect, HttpResponse
from .models import Game
from .forms import CustomUserCreationForm, ProfileForm

# Try to import backend scripts (don’t crash if they’re missing)
# try:
#     from AddGameObject import main as add_games
#     from GetGameIds import GamesToday
# except ImportError as e:
#     print("⚠️ Could not import backend scripts from Backend/BackendDB:", e)
#     def add_games(): 
#         pass
#     def GamesToday(): 
#         pass

Weeks = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
#temp team holder
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
def home(request):
    Games = Game.objects.all()
    last_saved_week = request.session.get('saved_week', 1) #Retrieve the last viewed week, otherwise use default week
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
       
        if fav_teams== []:
            team = 1
        else:
            team = fav_teams[0]
    else:
        team=None
    context = {"Games": Games, "Weeks": Weeks, "saved" : last_saved_week,"Team":team}
    return render(request, 'main.html', context)

def week(request, num):
    Games = Game.objects.filter(Week=f"Week {num}")
    request.session['saved_week'] = num #Save the last viewed week into request
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
       
        if fav_teams== []:
            team = 1
        else:
            team = fav_teams[0]
    else:
        team=None
    return render(request, 'week.html', {"Games": Games, "week_number": num, "Weeks": Weeks,"Team":team})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Welcome to Half-Time, your account has been created")
            return render(request, "register.html", {'form': form,})
        else:
            currenterrors=dict(form.errors)
            errors =[]
            for errornames in currenterrors.values():
                for error in errornames:
                    errors.append(error)
            messages.error(request,"Error")
            return render(request, "register.html", {'form': form, "Weeks": Weeks,"errors":errors})     
            print(form.errors)
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
                if action == 'add':
                    if selected_team not in favorites:
                        favorites.append(selected_team)
                        request.session['favorite_teams'] = favorites
                elif action == 'remove':
                    if selected_team in favorites:
                        favorites.remove(selected_team)
                        request.session['favorite_teams'] = favorites

            request.session['favorite_teams'] = favorites
            return redirect('pickteam')

        Profile.objects.filter(user=current_user.user).update(favorite_team={"fav_teams": favorites})

        return render(request, "newuserhub.html", {"Weeks": Weeks, "Teams": nfl_teams, "Favorites": favorites, "currentuser": current_user, "Team": team})
    else:
        return render(request, "newuserhub.html", {"Weeks": Weeks, "Teams": nfl_teams})

def user_account(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user.id)
        fav_teams = current_user.favorite_team["fav_teams"]
       
        if fav_teams== []:
            team = 1
        else:
            team = fav_teams[0]
    else:
        team=None

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
    else:
        return render(request, 'account.html',{"Weeks":Weeks,"Team":team})



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







def fav_team_games(request,team):
        
    current_user=Profile.objects.get(user=request.user.id)
    fav_teams = current_user.favorite_team["fav_teams"]
    Games= Game.objects.filter(Q(HomeTeam=f"{team}") | Q(AwayTeam=f"{team}"))
    
    return render(request, "favteamgames.html", {"Games": Games,  "Weeks": Weeks,"Favs":fav_teams,"Current_Team":team,"Team":team})

  



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user=request.user.id)
            current_login_count = current_user.login_count 

            if current_login_count == 0:
                Profile.objects.filter(user=request.user.id).update(login_count=current_login_count+1)
                return redirect("pickteam")
            else:
                Profile.objects.filter(user=request.user.id).update(login_count=current_login_count+1)

                return redirect("home")
        else:
            messages.error(request, 'The username or password (or both) is invaild. Please enter the correct credentials.')
            return redirect('login')
    


    return render(request, "login.html",{"Weeks": Weeks})

def logout_view(request):
    logout(request)
    return redirect("home")   

# def refresh_scores(request):
#     """Manually refresh the NFL scores."""
#     if request.method == "POST":
#         try:
#             GamesToday()   # fetch today/tomorrow IDs
#             add_games()    # update/create Game entries
#         except Exception as e:
#             print("Error refreshing scores:", e)
#     return redirect('home')







def GameSummary(Gameid):
   


    if not  GameData.objects.filter(GameID=Gameid).exists():
        print("Fetching data from API for GameID:", Gameid)
        Gameid=str(Gameid)
        conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
        print("Loaded API_KEY:", KEY)
        headers = {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': KEY
            }

        conn.request("GET", f"/games/statistics/teams?id={Gameid}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        decoded =data.decode("utf-8")
        parsed = json.loads(decoded)
        if parsed["results"]==0:
           return ("CANT add game")
        
        GameData.objects.create(GameID=Gameid, data=parsed)

        return (
            
            {"HomeTeam":parsed["response"][0],
            
            
            "AwayTeam":parsed["response"][1]
            
            
            }
            )
    else:  
      
        data =  GameData.objects.get(GameID=Gameid).data
        
        return( 
              
            {"HomeTeam":data["response"][0],
            
            
            "AwayTeam":data["response"][1]
            }
    )
    
 

        ## sends json data back

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
            print("❌ ERROR in load_game_summary:")

            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)