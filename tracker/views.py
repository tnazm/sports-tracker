from django.http import HttpResponse
from django.shortcuts import render
from .models import Game

def admin_dashboard(request):
    return HttpResponse("<h1>Welcome to Half-Time Application</h1>")
    games = Game.objects.all().order_by("-date_game_played")
    return render(request, "tracker/admin_dashboard.html", {"games": games})
