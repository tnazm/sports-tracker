from django.db import models

class Games(models.Models):
    player_name=models.CharField(max_length=100)
    opponent_name=models.CharField(max_length=100)
    sport=models.CharField(max_length=50)
    date_game_played=models.DateField()
    score=model.CharField(max_length=20)
    sport=models.model.CharField(max_length=20)
    result=models.CharField(max_length=10, options=[
        ('Win,Lose')
        ('Lose, Win')
        ('Draw,Draw')
    ]
    )
    def__str__(self):
        return f'{self.player_name} vs {self.opponent_name} on {self.date_game_played}

