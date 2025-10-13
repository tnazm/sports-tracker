from django.shortcuts import render, HttpResponse
from .models import Game
Weeks =["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
# Create your views here.
def home(request):
    return render(request, 'main.html')
def week1(request):
    Games = Game.objects.filter(Week="Week 1")
    return render(request, 'week.html',{"Games":Games,"week_number":1,"Weeks":Weeks})
def week2(request):
    Games = Game.objects.filter(Week="Week 2")
    return render(request, 'week.html',{"Games":Games,"week_number":2,"Weeks":Weeks})
def week3(request):
    Games = Game.objects.filter(Week="Week 3")
    return render(request, 'week.html',{"Games":Games,"week_number":3,"Weeks":Weeks})
def week4(request):
    Games = Game.objects.filter(Week="Week 4")
    return render(request, 'week.html',{"Games":Games,"week_number":4,"Weeks":Weeks})
def week5(request):
    Games = Game.objects.filter(Week="Week 5")
    return render(request, 'week.html',{"Games":Games,"week_number":5,"Weeks":Weeks})
def week6(request):
    Games = Game.objects.filter(Week="Week 6")
    return render(request, 'week.html',{"Games":Games,"week_number":6,"Weeks":Weeks})
def week7(request):
    Games = Game.objects.filter(Week="Week 7")
    return render(request, 'week.html',{"Games":Games,"week_number":7,"Weeks":Weeks})
def week8(request):
    Games = Game.objects.filter(Week="Week 8")
    return render(request, 'week.html',{"Games":Games,"week_number":8,"Weeks":Weeks})
def week9(request):
    Games = Game.objects.filter(Week="Week 9")
    return render(request, 'week.html',{"Games":Games,"week_number":9,"Weeks":Weeks})
def week10(request):
    Games = Game.objects.filter(Week="Week 10")
    return render(request, 'week.html',{"Games":Games,"week_number":10,"Weeks":Weeks})
def week11(request):
    Games = Game.objects.filter(Week="Week 11")
    return render(request, 'week.html',{"Games":Games,"week_number":11,"Weeks":Weeks})
def week12(request):
    Games = Game.objects.filter(Week="Week 12")
    return render(request, 'week.html',{"Games":Games,"week_number":12,"Weeks":Weeks})
def week13(request):
    Games = Game.objects.filter(Week="Week 13")
    return render(request, 'week.html',{"Games":Games,"week_number":13,"Weeks":Weeks})
def week14(request):
    Games = Game.objects.filter(Week="Week 14")
    return render(request, 'week.html',{"Games":Games,"week_number":14,"Weeks":Weeks})
def week15(request):
    Games = Game.objects.filter(Week="Week 15")
    return render(request, 'week.html',{"Games":Games,"week_number":15,"Weeks":Weeks})
def week16(request):
    Games = Game.objects.filter(Week="Week 16")
    return render(request, 'week.html',{"Games":Games,"week_number":16,"Weeks":Weeks})
def week17(request):
    Games = Game.objects.filter(Week="Week 17")
    return render(request, 'week.html',{"Games":Games,"week_number":17,"Weeks":Weeks})
def week18(request):
    Games = Game.objects.filter(Week="Week 18")
    return render(request, 'week.html',{"Games":Games,"week_number":18,"Weeks":Weeks})
