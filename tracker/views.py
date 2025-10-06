from django.shortcuts import render
from .models import Games

# Create your views here.
def _dashboard_(request):
    game=Games.objects.all().order_ny("-Date played")
    return render(request, 'tracker/admin__dashboard.html',{'games':game})
    