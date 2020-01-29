from django.test import TestCase
from ctl.models import *
import random
import datetime



# Create your tests here.
def rotate(li):
	l = li[:]
	temp = l.pop()
	l = l[0:1] + [temp] + l[1:]
	return l

class CreateNewSeason(TestCase):

    def setUp(self):
        pass

    def test_DeleteLineUps(self):
        self.assertTrue(len(Lineup.objects.all()) != 0)
        Lineup.objects.all().delete()
        self.assertTrue(len(Lineup.objects.all()) == 0)

    def test_DeleteMatchups(self):
        self.assertTrue(len(Matchup.objects.all()) != 0)
        Matchup.objects.all().delete()
        self.assertTrue(len(Matchup.objects.all()) == 0)

    def test_DeleteResultSets(self):
        self.assertTrue(len(ResultSet.objects.all()) != 0)
        ResultSet.objects.all().delete()
        self.assertTrue(len(ResultSet.objects.all()) == 0)

    def test_DeleteMatchReports(self):
        self.assertTrue(len(MatchReport.objects.all()) != 0)
        MatchReport.objects.all().delete()
        self.assertTrue(len(MatchReport.objects.all()) == 0)

    def test_DeleteMapss(self):
        self.assertTrue(len(Maps.objects.all()) != 0)
        Maps.objects.all().delete()
        self.assertTrue(len(Maps.objects.all()) == 0)

    def test_CreateMapss(self):
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


        self.assertTrue(len(Maps.objects.all()) == num_weeks)

    def test_CreateMatchups(self):
        print()
        Maps.objects.all().delete()
        num_weeks = 10
        season_start_date = datetime.datetime(2019, 12, 2, 21, 0, 0, 0, datetime.timezone.utc)
        for i in range(num_weeks):
            Maps.objects.create(week=i+1, maps="Test", start_date = season_start_date + (i * datetime.timedelta(days=7)))

        #print(f"HERE ------------ <{len(Maps.objects.all())}> ----------------")

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


        for obj in Matchup.objects.all().order_by('week__week'):
            print(obj)






