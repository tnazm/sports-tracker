from django.contrib import admin
from .models import Games

# Register your models here.
class Games_Admin(admin.ModelAdmin):
    variables=('player_name','opponent_name', 'sport','date_game_played','score', 'result')
    
