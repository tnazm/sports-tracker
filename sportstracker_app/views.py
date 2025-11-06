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
from sportstracker_app.models import GameData
load_dotenv()
KEY = os.getenv("API_KEY")

BACKEND_PATH = Path(settings.BASE_DIR) / "Backend" / "BackendDB"
BACKEND_PATH_STR = str(BACKEND_PATH.resolve())

if BACKEND_PATH_STR not in sys.path:
    sys.path.insert(0, BACKEND_PATH_STR)

from django.shortcuts import render, redirect, HttpResponse
from .models import Game
from .forms import CustomUserCreationForm

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
            return render(request, "login.html", {'form': form, "Weeks": Weeks})
        else:
            print(form.errors)
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
            messages.error(request, 'Invalid credentials')
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