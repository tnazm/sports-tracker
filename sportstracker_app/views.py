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

def week1(request):
    Games = Game.objects.filter(Week="Week 1")
    return render(request, 'week.html',{"Games":Games})
def week2(request):
    Games = Game.objects.filter(Week="Week 2")
    return render(request, 'week.html',{"Games":Games})

def week3(request):
    Games = Game.objects.filter(Week="Week 3")
    return render(request, 'week.html',{"Games":Games})
def week4(request):
    Games = Game.objects.filter(Week="Week 4")
    return render(request, 'week.html',{"Games":Games})
def week5(request):
    Games = Game.objects.filter(Week="Week 5")
    return render(request, 'week.html',{"Games":Games})
def week6(request):
    Games = Game.objects.filter(Week="Week 6")
    return render(request, 'week.html',{"Games":Games})
def week7(request):
    Games = Game.objects.filter(Week="Week 7")
    return render(request, 'week.html',{"Games":Games})
def week8(request):
    Games = Game.objects.filter(Week="Week 8")
    return render(request, 'week.html',{"Games":Games})
def week9(request):
    Games = Game.objects.filter(Week="Week 9")
    return render(request, 'week.html',{"Games":Games})
def week10(request):
    Games = Game.objects.filter(Week="Week 10")
    return render(request, 'week.html',{"Games":Games})
def week11(request):
    Games = Game.objects.filter(Week="Week 11")
    return render(request, 'week.html',{"Games":Games})
def week12(request):
    Games = Game.objects.filter(Week="Week 12")
    return render(request, 'week.html',{"Games":Games})
def week13(request):
    Games = Game.objects.filter(Week="Week 13")
    return render(request, 'week.html',{"Games":Games})
def week14(request):
    Games = Game.objects.filter(Week="Week 14")
    return render(request, 'week.html',{"Games":Games})
def week15(request):
    Games = Game.objects.filter(Week="Week 15")
    return render(request, 'week.html',{"Games":Games})
def week16(request):
    Games = Game.objects.filter(Week="Week 16")
    return render(request, 'week.html',{"Games":Games})
def week17(request):
    Games = Game.objects.filter(Week="Week 17")
    return render(request, 'week.html',{"Games":Games})

def week18(request):
    Games = Game.objects.filter(Week="Week 18")
    return render(request, 'week.html',{"Games":Games})
