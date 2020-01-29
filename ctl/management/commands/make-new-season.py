from django.test import TestCase
from django.core.management.base import BaseCommand, CommandError
from ctl.models import *
import random
import datetime

def rotate(li):
	l = li[:]
	temp = l.pop()
	l = l[0:1] + [temp] + l[1:]
	return l

class Command(BaseCommand):
    help = 'Starts a new season. Remember to edit the script!'
    
    def handle(self, *args, **options):
        Lineup.objects.all().delete()
        Matchup.objects.all().delete()
        ResultSet.objects.all().delete()
        MatchReport.objects.all().delete()
        Maps.objects.all().delete()
        num_weeks = 13
        season_start_date = datetime.datetime(2019, 12, 2, 21, 0, 0, 0, datetime.timezone.utc)
        maps_list = [
            "Nightshade LE/Triton LE/Eternal Empire LE/Ephemeron LE/Simulacrum LE/World of Sleepers LE/Zen LE",
            "Eternal Empire LE/Ephemeron LE/World of Sleepers LE/Zen LE/Nightshade LE/Triton LE/Simulacrum LE",
            "World of Sleepers LE/Zen LE/Triton LE/Simulacrum LE/Eternal Empire LE/Ephemeron LE/Nightshade LE",
            "Triton LE/Simulacrum LE/Ephemeron LE/Nightshade LE/World of Sleepers LE/Zen LE/Eternal Empire LE",
            "Ephemeron LE/Nightshade LE/Zen LE/Eternal Empire LE/Triton LE/Simulacrum LE/World of Sleepers LE",
            "Zen LE/Eternal Empire LE/Simulacrum LE/World of Sleepers LE/Ephemeron LE/Nightshade LE/Triton LE",
            "Simulacrum LE/World of Sleepers LE/Nightshade LE/Triton LE/Zen LE/Eternal Empire LE/Ephemeron LE",
            ]
        for i in range(num_weeks):
            Maps.objects.create(week=i+1, maps=maps_list[i%7], start_date = season_start_date + (i * datetime.timedelta(days=7)))
    
        group1 = ['Born Gosu', 'The Gosu Crew', 'SC2 Swarm', 'Validity Gaming', 'Formless Bearsloths', 'Team UnRivaled']
        group2 = ['Taste The Bacon', 'Guns and Roaches', 'JaM iT Gaming', 'Daily Life', 'All-Inspiration', 'Alpha X']
    
        groups = [group1, group2]
    
        random.shuffle(groups[0])
        random.shuffle(groups[1])
    
        for group in groups:
            for i in range(len(group)-1):
                for j in range(len(group)//2):
                    week = Maps.objects.get(week=i+1)
                    #print(i)
                    team1 = Roster.objects.get(team_name=group[j])
                    team2 = Roster.objects.get(team_name=group[-(j+1)])
    
                    Matchup.objects.create(week=week, team1=team1, team2=team2)
    
                group = rotate(group)
    
        random.shuffle(groups[0])
        random.shuffle(groups[1])
    
        for group in groups:
            for i in range(len(group)-1):
                for j in range(len(group)//2):
                    week = Maps.objects.get(week=i+6)
                    #print(i)
                    team1 = Roster.objects.get(team_name=group[j])
                    team2 = Roster.objects.get(team_name=group[-(j+1)])
    
                    Matchup.objects.create(week=week, team1=team1, team2=team2)
    
                group = rotate(group)
                
        self.stdout.write(self.style.SUCCESS('Season created. Please confirm all information is accurate.'))