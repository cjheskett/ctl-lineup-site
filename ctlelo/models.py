from django.db import models

# Create your models here.
class Roster(models.Model):
    team_name = models.CharField(max_length=50)
    team_abrv = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.team_name


class Player(models.Model):
    ZERG = 'Z'
    PROTOSS = 'P'
    TERRAN = 'T'
    RANDOM = 'R'
    RACE_CHOICES = (
        (ZERG, 'Zerg'),
        (PROTOSS, 'Protoss'),
        (TERRAN, 'Terran'),
        (RANDOM, 'Random'),
    )

    LEAGUE_CHOICES = (
        (0, 'Bronze'),
        (1, 'Silver'),
        (2, 'Gold'),
        (3, 'Platinum'),
        (4, 'Diamond'),
        (5, 'Master'),
        (6, 'Grandmaster'),
    )


    team = models.ForeignKey(Roster, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    league = models.IntegerField(choices=LEAGUE_CHOICES)
    race = models.CharField(max_length=1, choices=RACE_CHOICES)
    elo = models.IntegerField(default=1500)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.name + "[" + self.team.team_abrv + "] "

    def display(self):
        return '[' + self.team.team_abrv + '] ' + self.name +  ' | ' +  str(self.wins) + "-" + str(self.losses) + ' | Elo: ' + str(self.elo)

    def reset(self):
        self.elo = 1500
        self.wins = 0
        self.losses = 0

class Game(models.Model):
    player1 = models.ForeignKey(Player, related_name="player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name="player2", on_delete=models.CASCADE)

    WINNER = (
        (1, "Player 1"),
        (2, "Player 2"),
        )
    date_added = models.DateTimeField(auto_now_add=True)
    winner = models.IntegerField(choices=WINNER)

    season = models.IntegerField()
    week = models.IntegerField()
    def __str__(self):
        if self.winner == 1:
            return '[' + str(self.date_added) + '] (W) ' + str(self.player1) + ' vs (L) ' + str(self.player2)
        else:
            return '[' + str(self.date_added) + '] (L) ' + str(self.player1) + ' vs (W) ' + str(self.player2)


