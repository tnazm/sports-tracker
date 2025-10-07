from django.db import models

class Game(models.Model):
    GameID = models.CharField(max_length=50, unique=True)
    HomeTeam = models.CharField(max_length=25)
    AwayTeam = models.CharField(max_length=25)
    HomeScore = models.IntegerField()
    AwayScore = models.IntegerField()



    def __str__(self):
        return f'{self.player_name} vs {self.opponent_name} on {self.date_game_played}'
