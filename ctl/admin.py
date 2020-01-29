from django.contrib import admin

# Register your models here.
from .models import Player, Roster, Captain, Maps, Lineup, Matchup, MatchReport, ResultSet

admin.site.register(Player)
admin.site.register(Roster)
admin.site.register(Captain)
admin.site.register(Maps)
admin.site.register(Lineup)
admin.site.register(Matchup)
admin.site.register(MatchReport)
admin.site.register(ResultSet)