from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'main.html')

def games_page(request):
    return render(request, 'games.html')
