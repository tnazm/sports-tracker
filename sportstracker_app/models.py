from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    GameID = models.CharField(max_length=50,unique=True)
    HomeTeam = models.CharField(max_length=75)
    AwayTeam = models.CharField(max_length=75)
    HomeScore = models.IntegerField()
    AwayScore = models.IntegerField()
    Week = models.CharField(max_length=15,null=True,blank=True,default="missing")
    date = models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.HomeTeam} vs {self.AwayTeam} on {self.date}'


class HoldIDs(models.Model):
    GameID = models.CharField(max_length=50,unique=True)
    week = models.CharField(max_length=15)
    date = models.DateField()

    def __str__(self):
        return self.GameID
    
class GameData(models.Model):
    GameID = models.CharField(max_length=50)
    data = models.JSONField()

    def __str__(self):
        return f'GameData for GameID: {self.GameID}'

#This is for the user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)    