from django.shortcuts import render, HttpResponse
from .models import Game

# Create your views here.
def home(request):
    Weeks =["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
    Games = Game.objects.all()
    context={
        "Games":Games,
        "Weeks":Weeks
    }
    return render(request, 'main.html',context)   
