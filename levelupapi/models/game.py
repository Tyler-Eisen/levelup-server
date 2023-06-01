from django.db import models
from .game_type import GameType
from .gamer import Gamer


class Game(models.Model):
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
