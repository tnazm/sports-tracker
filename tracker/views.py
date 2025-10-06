from django.shortcuts import render
from .models import Game

def admin_dashboard(request):
    games = Game.objects.all().order_by("-date_game_played")
    return render(request, "tracker/admin_dashboard.html", {"games": games})
