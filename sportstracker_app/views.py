import sys
from pathlib import Path
from django.conf import settings

# Point Python at: <project>/Backend/BackendDB
BACKEND_PATH = Path(settings.BASE_DIR) / "Backend" / "BackendDB"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from django.shortcuts import render, redirect
from .models import Game

# Try to import backend scripts (don’t crash if they’re missing)
try:
    from AddGameObject import main as add_games
    from GetGameIds import GamesToday
except ImportError as e:
    print("⚠️ Could not import backend scripts from Backend/BackendDB:", e)
    def add_games(): 
        pass
    def GamesToday(): 
        pass

Weeks = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]

def home(request):
    Games = Game.objects.all()
    context = {"Games": Games, "Weeks": Weeks}
    return render(request, 'main.html', context)

def week(request, num):
    Games = Game.objects.filter(Week=f"Week {num}")
    return render(request, 'week.html', {"Games": Games, "week_number": num, "Weeks": Weeks})

def refresh_scores(request):
    """Manually refresh the NFL scores."""
    if request.method == "POST":
        try:
            GamesToday()   # fetch today/tomorrow IDs
            add_games()    # update/create Game entries
        except Exception as e:
            print("Error refreshing scores:", e)
    return redirect('home')
