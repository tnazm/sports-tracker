from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'opponent_name', 'sport', 'date_game_played', 'score', 'result')
