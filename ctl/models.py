from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#from django.core.exceptions import RelatedObjectDoesNotExist

# Create your models here.
class Captain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey("Roster", on_delete=models.CASCADE, null=True, blank=True)
    is_admin = models.BooleanField()
    def __str__(self):
        if not self.is_admin:
            return '[' + self.team.team_abrv + '] ' + self.user.username
        else:
            return '[ADMIN] ' + self.user.username

class Roster(models.Model):
    team_name = models.CharField(max_length=50)
    team_abrv = models.CharField(max_length=10, null=True)
    wiki_name = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    icon_url = models.URLField(max_length=200)
    def __str__(self):
        return self.team_name
    #team_captain = models.OneToOneField("Player",on_delete=models.CASCADE)


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
        (7, 'Bench'),
    )

    team = models.ForeignKey(Roster, on_delete=models.CASCADE)
    bnet_name = models.CharField(max_length=100)
    sc2_name = models.CharField(max_length=50)
    ctl_url = models.URLField(max_length=100)
    league = models.IntegerField(choices=LEAGUE_CHOICES)
    race = models.CharField(max_length=1, choices=RACE_CHOICES)
    is_captain = models.BooleanField()

    def __str__(self):
        return self.sc2_name + ' | ' + self.bnet_name + ' (' + self.race + ')'

    def get_full_info(self):
        return '[' + str(self.team.team_abrv) + '] (' + self.race + ') ' + self.sc2_name + ' | ' + self.bnet_name

    def wiki(self):
        ret = 'CTL Roster Code: '
        race_dict = {'R': 'https://i.imgur.com/y6wDt.png', 'T': 'http://i.imgur.com/PZaHh.png', 'Z':'http://i.imgur.com/HRNlj.png', 'P': 'http://i.imgur.com/lY0rg.png'}
        ret += race_dict[self.race] + " [" + self.ctl_url + " " + self.sc2_name + ' | ' + self.bnet_name + "] <br />"
        return ret

class Lineup(models.Model):
    set1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set1", null=True, blank=True)
    set2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set2", null=True, blank=True)
    set3 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set3", null=True, blank=True)
    set4 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set4", null=True, blank=True)
    set5 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set5", null=True, blank=True)
    set6 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set6", null=True, blank=True)
    set7 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="set7", null=True, blank=True)

    team = models.ForeignKey(Roster, on_delete=models.CASCADE)
    week = models.ForeignKey("Maps", on_delete=models.CASCADE)
    submit_time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return "Week " + str(self.week.week) + " | " + str(self.team.team_abrv)

    def get_all_players(self):
        ret = []
        ret.append(self.set1)
        ret.append(self.set2)
        ret.append(self.set3)
        ret.append(self.set4)
        ret.append(self.set5)
        ret.append(self.set6)
        ret.append(self.set7)

        return ret

class Maps(models.Model):
    week = models.IntegerField()
    maps = models.CharField(max_length = 1000)
    start_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return "Week " + str(self.week)

    def is_current_week(self):
        if timezone.now() > self.start_date and self.start_date >= timezone.now() - datetime.timedelta(days=7): #if the current date is after the start_date but less than 7 days after it
            return True
        else:
            return False

class Matchup(models.Model):
    week = models.ForeignKey(Maps, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Roster, related_name="team1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Roster, related_name="team2", on_delete=models.CASCADE)

    def __str__(self):
        return "(" + str(self.week) + ") " + str(self.team1) + " vs " + str(self.team2)

class MatchReport(models.Model):
    WIN = 'win'
    LOSS = 'loss'
    ADMIN = 'admin'
    NOT_PLAYED = 'na'
    RESULT_CHOICES = (
        (WIN, 'Win'),
        (LOSS, 'Loss'),
        (ADMIN, 'Admin'),
        (NOT_PLAYED, 'N/A'),
    )
    team = models.ForeignKey(Roster, on_delete=models.CASCADE)
    week = models.ForeignKey(Maps, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(default=timezone.now())
    comments = models.CharField(max_length=100000)
    set1result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set2result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set3result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set4result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set5result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set6result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set71result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set72result = models.CharField(max_length=10, choices = RESULT_CHOICES)
    set73result = models.CharField(max_length=10, choices = RESULT_CHOICES)


    set71map = models.CharField(max_length=100)
    set72map = models.CharField(max_length=100)
    set73map = models.CharField(max_length=100)
    def __str__(self):
        return "(" + str(self.week) + ")" + " | " + str(self.team.team_abrv) + " | " + "Match Report"


class ResultSet(models.Model):
    week = models.ForeignKey(Maps, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Lineup, related_name="+", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Lineup, related_name="+", on_delete=models.CASCADE)
    team1_report = models.ForeignKey(MatchReport, related_name="+", on_delete=models.CASCADE, blank=True, null=True)
    team2_report = models.ForeignKey(MatchReport, related_name="+", on_delete=models.CASCADE, blank=True, null=True)
