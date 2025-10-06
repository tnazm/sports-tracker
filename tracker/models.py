from django.db import models

class Game(models.Model):
    player_name = models.CharField(max_length=100)
    opponent_name = models.CharField(max_length=100)
    sport = models.CharField(max_length=50)
    date_game_played = models.DateField()
    score = models.CharField(max_length=20)
    result = models.CharField(
        max_length=10,
        choices=[
            ('Win', 'Win'),
            ('Lose', 'Lose'),
            ('Draw', 'Draw'),
        ]
    )

    def __str__(self):
        return f'{self.player_name} vs {self.opponent_name} on {self.date_game_played}'
