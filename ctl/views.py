from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

import datetime

from .forms import NameForm
from .models import Player, Roster, Maps, Lineup, Matchup, MatchReport, ResultSet
#from django.db.models.fields.related_descriptors import RelatedObjectDoesNotExist

# Create your views here.

###############################################################################
#   If the user is an admin, return the admin menu.                           #
#   Otherwise, return the captain menu.                                       #
#   If the user does not exist, get them redirected to the login page.        #
###############################################################################
@login_required(redirect_field_name=None)
def index(request):
    try:
        if request.user.captain.is_admin:
            return render(request, 'ctl/index.html', {'admin':True})
        else:
            return render(request, 'ctl/index.html')
    except ObjectDoesNotExist as e:
        return render(request, 'ctl/index.html', {'not_auth':True})

###############################################################################
#  User request to be able to pet ducks after submitting a lineup.            #
###############################################################################
@login_required(redirect_field_name=None)
def pet_duck(request):
    return render(request, "ctl/pet_duck.html")

###############################################################################
#   Get the captain's team, and display it to them formatted.                 #
###############################################################################
@login_required(redirect_field_name=None)
def roster_test(request):
    team = request.user.captain.team
    golds = team.player_set.filter(league__lte = 2).order_by('race')
    plats = team.player_set.filter(league = 3).order_by('race')
    diamonds = team.player_set.filter(league = 4).order_by('race')
    masters = team.player_set.filter(league = 5).order_by('race')
    inactive = team.player_set.filter(league = 7).order_by('race')
    return render(request, "ctl/roster_test.html", {'team': team, 'golds': golds, 'plats': plats, "diamonds": diamonds, "masters": masters, "bench": inactive})


###############################################################################
#   If data not submitted, then display a form.                               #
#   Otherwise, get all info from the form, then create an object, checking    #
#   for identical players. If the user is an admin, then give them add. info  #
###############################################################################
@login_required(redirect_field_name=None)
def add_player(request):
    if 'team' not in request.POST:
        if request.user.captain.is_admin:
            teams = Roster.objects.all().order_by('team_name')
            return render(request, 'ctl/add_player.html', {'teams': teams})
        else:
            team = get_object_or_404(Roster, team_abrv = request.user.captain.team.team_abrv)
            return render(request, 'ctl/add_player.html', {'team': team})

    else:
        t = Roster.objects.get(team_name=request.POST['team'])
        bnet_id = request.POST['bnet_name']
        ctl_n = request.POST['ctl_name']
        ctl_u = request.POST['ctl_url']
        l = request.POST['league']
        r = request.POST['race']
        identical_players = Player.objects.filter(sc2_name__iexact=ctl_n, bnet_name__iexact=bnet_id)
        if len(identical_players) == 0:
            p = Player.objects.create(team=t, bnet_name=bnet_id, sc2_name=ctl_n, ctl_url=ctl_u, league=l, race=r, is_captain=False)
            if request.user.captain.is_admin:
                teams = Roster.objects.all()
                if p.team.team_abrv == "Teamless":
                    return render(request, 'ctl/add_player.html', {'teams': teams, 'no_team': True, 'wiki': p.wiki(), 'np_team': p.team})
                else:
                    return render(request, 'ctl/add_player.html', {'teams': teams, 'no_team': False, 'wiki': p.wiki(), 'np_team': p.team})
            else:
                team = get_object_or_404(Roster, team_abrv = request.user.captain.team.team_abrv)
                return render(request, 'ctl/add_player.html', {'team': team})
        else:
            if request.user.captain.is_admin:
                teams = Roster.objects.all().order_by('team_name')
                return render(request, 'ctl/add_player.html', {'teams': teams, "message": "That player already is in the database."})
            else:
                team = get_object_or_404(Roster, team_abrv = request.user.captain.team.team_abrv)
                return render(request, 'ctl/add_player.html', {'team': team, 'message': "That player already is in the database."})

###############################################################################
#   Similar to add_player, but the form searches for a player name.           #
#   If the user is a captain, they cannot edit a player not on their team.    #
###############################################################################
@login_required(redirect_field_name=None)
def edit_player(request):

    if request.method != 'POST' and 'pid' in request.GET:
        player = Player.objects.get(id=request.GET['pid'])
        if not request.user.captain.is_admin:
            if player.team != request.user.captain.team:
                return render(request, 'ctl/edit_player.html', {'message': "This player is not on your team!"})
        if request.user.captain.is_admin:
            teams = Roster.objects.all()
            return render(request, 'ctl/edit_player.html', {'teams': teams, 'player': player})
        else:
            return render(request, 'ctl/edit_player.html', {'player': player})
    else:
        if 'player_search' in request.POST:
            players_matching = None
            if request.user.captain.is_admin:
                players_matching = Player.objects.order_by(Lower('sc2_name')).filter(sc2_name__contains=request.POST['player_search'])
            else:
                players_matching = Player.objects.order_by(Lower('sc2_name')).filter(sc2_name__contains=request.POST['player_search'], team=request.user.captain.team)
            if len(players_matching) == 0:
                message = "No players matching that criteria were found. Please try again. If you're a captain, the player may exist, but is not currently on your roster.<br />"
                return render(request, 'ctl/edit_player.html', {'message': message})
            elif len(players_matching) == 1:
                player = players_matching[0]
                if request.user.captain.is_admin:
                    teams = Roster.objects.all()
                    return render(request, 'ctl/edit_player.html', {'teams': teams, 'player': player})
                else:
                    return render(request, 'ctl/edit_player.html', {'player': player})
            else: #more than 2 players were found matching the search criteria
                return render(request, 'ctl/edit_player.html', {'players': players_matching})

        elif 'team' not in request.POST:
                return render(request, 'ctl/edit_player.html')


        else:
            t = Roster.objects.get(team_name=request.POST['team'])
            bnet_id = request.POST['bnet_name']
            ctl_n = request.POST['ctl_name']
            ctl_u = request.POST['ctl_url']
            l = request.POST['league']
            r = request.POST['race']
            player = Player.objects.get(pk = request.POST['id'])
            player.team = t
            player.bnet_name = bnet_id
            player.sc2_name = ctl_n
            player.ctl_url = ctl_u
            player.league = l
            player.race = r
            player.save()
            return render(request, 'ctl/edit_player.html', {'message': "Player successfully edited."})

###############################################################################
#   Lets a captain select a player and remove them from their team.           #
###############################################################################
@login_required(redirect_field_name=None)
def remove_player(request):
    message = ''
    if 'player' in request.POST:
        player = Player.objects.get(pk = request.POST['player'])
        return render(request, 'ctl/remove_player.html', {'player': player})
    elif 'id' in request.POST:
        player = Player.objects.get(pk = request.POST['id'])
        no_team = Roster.objects.get(team_abrv = "Teamless")
        player.team = no_team
        player.save()
        message += "Player removed.<br />"
    try:
        team = get_object_or_404(Roster, team_abrv = request.user.captain.team.team_abrv)
        roster = team.player_set.all()
        return render(request, 'ctl/remove_player.html', {'roster': roster, 'message': message})
    except:
        return render(request, "ctl/remove_player.html", {'message': "You are not a captain. If you are a captain, please PM Kamarill ASAP."})


###############################################################################
#   The main user functionality of the system. This generates HTML and        #
#   MediaWiki formatted code so that admins can copy/paste lineups into the   #
#   respective areas. Lineups are submitted by captains. In addition, if      #
#   a captain failed to submit a lineup for the week, this duplicates their   #
#   previous lineups, and submits that for them if the admins select that     #
#   option.                                                                   #
###############################################################################
@login_required(redirect_field_name=None)
def view_lineups(request):
    if request.user.captain.is_admin:
        if 'week' not in request.POST:
            weeks = Maps.objects.all().order_by('week')
            return render(request, "ctl/view_lineups.html", {'weeks': weeks})
        else:
            message = ''
            week = Maps.objects.get(pk=request.POST['week'])
            matchups = Matchup.objects.filter(week=week)

            lineups_needed = []


            race_dict = {'R': 'https://i.imgur.com/y6wDt.png', 'T': 'http://i.imgur.com/PZaHh.png', 'Z':'http://i.imgur.com/HRNlj.png', 'P': 'http://i.imgur.com/lY0rg.png'}


            lineups = []
            maps = []
            maps.extend(week.maps.split('/'))
            continue_flag = False
            html_code = ''
            for m in matchups:
                try:
                    team1 = Lineup.objects.get(team=m.team1, week=m.week)
                except Lineup.DoesNotExist:
                    if 'make_old_lineups' not in request.POST:
                        lineups_needed.append(m.team1)
                        continue_flag = True
                    else:
                        try:
                            lp_copy = Lineup.objects.get(team=m.team1, week=Maps.objects.get(week=m.week.week-2))
                        except Lineup.DoesNotExist:
                            pass

                        try:
                            lp_copy = Lineup.objects.get(team=m.team1, week=Maps.objects.get(week=m.week.week-1))
                        except Lineup.DoesNotExist:
                            pass
                        lp_copy.week = m.week
                        lp_copy.pk=None
                        lp_copy.save()
                        team1 = lp_copy

                try:
                    team2 = Lineup.objects.get(team=m.team2, week=m.week)
                except Lineup.DoesNotExist:
                    if 'make_old_lineups' not in request.POST:
                        lineups_needed.append(m.team2)
                        continue_flag = True
                    else:
                        try:
                            lp_copy = Lineup.objects.get(team=m.team2, week=Maps.objects.get(week=m.week.week-2))
                        except Lineup.DoesNotExist:
                            pass

                        try:
                            lp_copy = Lineup.objects.get(team=m.team2, week=Maps.objects.get(week=m.week.week-1))
                        except Lineup.DoesNotExist:
                            pass

                        lp_copy.week = m.week
                        lp_copy.pk=None
                        lp_copy.save()
                        team2 = lp_copy

                if continue_flag:
                    continue_flag = False
                    continue

                team1_players = team1.get_all_players()
                team2_players = team2.get_all_players()
                lineups.append((team1, team2))
                html_code += '<h1><img src="%s"><font color="%s">%s</font> vs <font color="%s">%s</font><img src="%s"></h1><br />' % (m.team1.icon_url, m.team1.color, m.team1.team_abrv, m.team2.color, m.team2.team_abrv, m.team2.icon_url)
                for i in range(7):
                    combined_name1 = team1_players[i].sc2_name + ' | ' + team1_players[i].bnet_name
                    combined_name2 = team2_players[i].sc2_name + ' | ' + team2_players[i].bnet_name
                    html_code += '<img src="%s"> <a href="%s">%s</a> vs. <a href="%s">%s</a> <img src="%s"> <i>[%s]</i><br />' % (race_dict[team1_players[i].race], team1_players[i].ctl_url, combined_name1, team2_players[i].ctl_url, combined_name2, race_dict[team2_players[i].race], maps[i])
                html_code += '<br /><br />'

            if len(lineups_needed) > 0:
                message = "<p>Cannot process lineups for " + str(week) + " at this time. Lineups are still needed from these teams:</p><ul>"
                for l in lineups_needed:
                    message += ('<li>' + str(l) + '</li>')
                message += "</ul><br />"
                make_old_lineups = False
                if week.week > 1:
                    make_old_lineups = True
                    for team in lineups_needed:
                        try:
                            old_lineup = Lineup.objects.get(team=team, week=Maps.objects.get(week=week.week-1))
                        except Lineup.DoesNotExist:
                            if week.week > 2:
                                try:
                                    old_lineup = Lineup.objects.get(team=team, week=Maps.objects.get(week=week.week-2))
                                except Lineup.DoesNotExist:
                                    make_old_lineups = False
                                    message += "<p>This team has no valid old lineup to copy: %s</p>" % str(team.team_name)
                                    #break
                            else:
                                make_old_lineups = False
                                message += "<p>This team has no valid old lineup to copy: %s</p>" % str(team.team_name)

                    #make_old_lineups = True
                return render(request, "ctl/view_lineups.html", {'message': message, 'weeks': Maps.objects.all().order_by('week'), 'make_old_lineups': make_old_lineups, "req_week": week})

            first_lineup = lineups.pop(0)



            return render(request, "ctl/view_lineups.html", {'matchups': lineups, 'maps': maps, "week": week.week, "first_lineup": first_lineup, "html_code": html_code})
    else:
        return HttpResponse("You shouldn't be here.")


@login_required(redirect_field_name=None)
def view_lineups_blank(request):
    if request.user.captain.is_admin:
        if 'week' not in request.POST:
            weeks = Maps.objects.all().order_by('week')
            return render(request, "ctl/view_lineups_blank.html", {'weeks': weeks})
        else:
            message = ''
            week = Maps.objects.get(pk=request.POST['week'])
            matchups = Matchup.objects.filter(week=week)

            lineups = []
            maps = []
            maps.extend(week.maps.split('/'))
            html_code = ''
            for m in matchups:
                lineups.append((m.team1, m.team2))



            first_lineup = lineups.pop(0)



            return render(request, "ctl/view_lineups_blank.html", {'matchups': lineups, 'maps': maps, "week": week.week, "first_matchup": first_lineup, "html_code": html_code, "message": message})
    else:
        return HttpResponse("You shouldn't be here.")

###############################################################################
#   This creates a result_set object, used to display match reports, which    #
#   admins use to create results for the week.                                #
###############################################################################
@login_required(redirect_field_name=None)
def view_match_reports(request):
    if request.user.captain.is_admin:
        if 'week' not in request.POST:
            weeks = Maps.objects.all().order_by('week')
            return render(request, "ctl/view_match_reports.html", {'weeks': weeks})
        else:
            week = Maps.objects.get(pk=request.POST['week'])
            results = ResultSet.objects.filter(week=week)
            results.delete()
            matchups = Matchup.objects.filter(week=week)
            maps = []
            maps.extend(week.maps.split('/'))
            team1_report = None
            team2_report = None
            for m in matchups:
                team1 = Lineup.objects.get(team=m.team1, week=m.week)
                team2 = Lineup.objects.get(team=m.team2, week=m.week)
                try:
                    team1_report = MatchReport.objects.get(team=m.team1, week=m.week)
                except ObjectDoesNotExist:
                    team1_report = MatchReport.objects.create(team=team1.team, week=week, submit_time=timezone.now(), comments="Boy I should have submitted a match report!", set1result='na', set2result='na', set3result='na', set4result='na', set5result='na', set6result='na', set71result='na', set72result='na', set73result='na', set71map='na', set72map='na', set73map='na')

                try:
                    team2_report = MatchReport.objects.get(team=m.team2, week=m.week)
                except ObjectDoesNotExist: #if len(team2_report) == 0:
                    team2_report = MatchReport.objects.create(team=team2.team, week=week, submit_time=timezone.now(), comments="Boy I should have submitted a match report!", set1result='na', set2result='na', set3result='na', set4result='na', set5result='na', set6result='na', set71result='na', set72result='na', set73result='na', set71map='na', set72map='na', set73map='na')

                ResultSet.objects.create(week=week, team1=team1, team2=team2, team1_report=team1_report, team2_report=team2_report)
            return render(request, "ctl/view_match_reports.html", {'maps': maps, "results": results})
    else:
        return HttpResponse("You shouldn't be here.")


###############################################################################
#   Old function which generates an lineup for manual submission. Unused.     #
###############################################################################
@login_required(redirect_field_name=None)
def create_typeform(request):
    try:
        team = request.user.captain.team
        golds = team.player_set.filter(league__lte = 2)
        plats = team.player_set.filter(league__lte = 3)
        diamonds = team.player_set.filter(league = 4)
        masters = team.player_set.filter(league = 5)
        weeks = Maps.objects.all()
        maps = []
        for w in weeks:
            if w.is_current_week():
                maps.extend(w.maps.split('/'))

        return render(request, "ctl/create_typeform.html", {'team': team, 'golds': golds, 'plats': plats, "diamonds": diamonds, "masters": masters, "maps": maps})
    except:
       return render(request, "ctl/create_typeform.html", {'message': "You are not a captain. If you are a captain, please PM Kamarill ASAP."})

###############################################################################
#   Displays a form for lineup submission, and if data is present, submit the #
#   lineup.                                                                   #
###############################################################################
@login_required(redirect_field_name=None)
def submit_lineup(request):
    if 'set1' in request.POST:
        message = ''
        t = request.user.captain.team
        weeks = Maps.objects.all()
        maps = []
        wk = None
        for w in weeks:
            if w.is_current_week():
                wk = w
                maps.extend(w.maps.split('/'))

        s1 = Player.objects.get(id=request.POST['set1'])
        s2 = Player.objects.get(id=request.POST['set2'])
        s3 = Player.objects.get(id=request.POST['set3'])
        s4 = Player.objects.get(id=request.POST['set4'])
        s5 = Player.objects.get(id=request.POST['set5'])
        s6 = Player.objects.get(id=request.POST['set6'])
        s7 = Player.objects.get(id=request.POST['set7'])
        players = []
        players.append(s1)
        players.append(s2)
        players.append(s3)
        players.append(s4)
        players.append(s5)
        players.append(s6)
        players.append(s7)

        new_lineup = Lineup(team=t, week = wk, set1=s1, set2=s2, set3=s3, set4=s4, set5=s5, set6=s6, set7=s7, submit_time=timezone.now())
        old_lineups = Lineup.objects.filter(team=t).filter(week=wk)
        for l in old_lineups:
            l.delete()
        new_lineup.save()
        lineup_text = ''
        for i in range(7):
            lineup_text += "Set " + str(i+1) + ' - ' + players[i].sc2_name + ", " + players[i].bnet_name + ' - ' + players[i].race + ' - ' + maps[i] + '<br />'

        #if '@' in request.user.email:
        #    send_mail('Your Lineup for Week %s' % new_lineup.week, message, 'dkamarill@gmail.com', [request.user.email], fail_silently=True)
        return render(request, "ctl/submit_lineup.html", {'lineup': new_lineup, 'lineup_text': lineup_text})
    else:
        try:
            team = request.user.captain.team
            golds = team.player_set.filter(league__lte = 3)
            plats = team.player_set.filter(league__lte = 3)
            diamonds = team.player_set.filter(league = 4)
            masters = team.player_set.filter(league = 5)
            bench = team.player_set.filter(league = 7)
            weeks = Maps.objects.all()
            maps = []
            for w in weeks:
                if w.is_current_week():
                    maps.extend(w.maps.split('/'))

            return render(request, "ctl/submit_lineup.html", {'team': team, 'golds': golds, 'plats': plats, "diamonds": diamonds, "masters": masters,"bench": bench, "maps": maps})
        except:
           return render(request, "ctl/submit_lineup.html", {'message': "You are not a captain. If you are a captain, please PM Kamarill ASAP."})


###############################################################################
#   This function was used to convert the old roster page (BBCode) to Django  #
#   model objects, to avoid manual entry. Unused today.                       #
###############################################################################
@login_required(redirect_field_name=None)
def bulk_add(request, team):
    if 'text' not in request.POST:
        return render(request, "ctl/bulk_add.html", {'team': team})
    else:
        test_message = ''
        players_to_add = request.POST['text']
        l = request.POST['league']
        t = Roster.objects.get(team_abrv=team)
        players_to_add_list = players_to_add.split('\n')
        for p in players_to_add_list:
            r = ''
            player = p.replace('[', '')
            player = player.replace(']', ' ')
            player_info = player.split(' ')

            if 'lY0rg' in player_info[0]:
                r = 'P'
            elif 'PZaHh' in player_info[0]:
                r = 'T'
            elif 'HRNlj' in player_info[0]:
                r = 'Z'
            else:
                r = 'R'

            ctl_u = player_info[1]
            ctl_n = player_info[2]
            bnet_id = player_info[4]
            new_player = Player(team=t, bnet_name=bnet_id, sc2_name=ctl_n, ctl_url=ctl_u, league=l, race=r, is_captain=False)
            players_with_name = Player.objects.filter(sc2_name=ctl_n, bnet_name=bnet_id)
            if players_with_name.count() == 0:
                new_player.save()
                test_message += (str(t) + ' ' + bnet_id + ' ' + ctl_n + ' ' + ctl_u + ' ' + l + ' ' + r + '<br />')
            else:
                test_message += ("Did not add player " + ctl_n + " due to database conflict.<br />")
        return render(request, "ctl/bulk_add.html", {'message': test_message, 'team': team})

def create_account(request):
    if 'username' not in request.POST:
        return render(request, "ctl/create_account.html")
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.create_user(username, email, password)
        except IntegrityError as e:
            return render(request, "ctl/create_account.html", {"message": "That username already exists. If this is an issue, please PM Kamarill ASAP."})
        return redirect('index')

def css_test(request):
    return render(request, "ctl/css_test.html")


###############################################################################
#   Very similar to submitting a lineup. Displays a form, and if data is      #
#   present, create a match report object.                                    #
###############################################################################
@login_required(redirect_field_name=None)
def submit_match_report(request):
    if 'week' not in request.POST:
        weeks = Maps.objects.exclude(start_date__gt=timezone.now() - datetime.timedelta(days=7))
        return render(request, "ctl/submit_match_report.html", {'weeks': weeks})
    elif 'set71' not in request.POST:
        week = Maps.objects.get(pk=request.POST['week'])
        lineup = Lineup.objects.get(week=week, team=request.user.captain.team)
        maps = []
        maps.extend(week.maps.split('/'))
        matchup = None
        opp_lineup = None
        try:
            matchup = Matchup.objects.get(week=week, team1=request.user.captain.team)
            opp_lineup = Lineup.objects.get(week=week, team=matchup.team2)
        except:
            matchup = Matchup.objects.get(week=week, team2=request.user.captain.team)
            opp_lineup = Lineup.objects.get(week=week, team=matchup.team1)

        return render(request, "ctl/submit_match_report.html", {'maps': maps, "week": week, "lineup":lineup, 'opp_lineup': opp_lineup})

    else:
        week = Maps.objects.get(pk=request.POST['week'])
        set1 = request.POST['set1']
        set2 = request.POST['set2']
        set3 = request.POST['set3']
        set4 = request.POST['set4']
        set5 = request.POST['set5']
        set6 = request.POST['set6']
        set71 = request.POST['set71']
        set72 = request.POST['set72']
        set73 = request.POST['set73']
        set71map = request.POST['set71map']
        set72map = request.POST['set72map']
        set73map = request.POST['set73map']

        comments = request.POST['comments']
        old_mr = MatchReport.objects.filter(team=request.user.captain.team).filter(week=week)
        for mr in old_mr:
            mr.delete()
        MatchReport.objects.create(team=request.user.captain.team, week=week, submit_time=timezone.now(), comments=comments, set1result=set1, set2result=set2, set3result=set3, set4result=set4, set5result=set5, set6result=set6, set71result=set71, set72result=set72, set73result=set73, set71map=set71map, set72map=set72map, set73map=set73map)
        weeks = Maps.objects.exclude(start_date__gt=timezone.now() - datetime.timedelta(days=7))
        return render(request, "ctl/submit_match_report.html", {'weeks': weeks, 'message': "Your match report was successfully submitted."})

###############################################################################
#   A very lazy and casual password reset. Requires me to create a token.     #
###############################################################################
def reset_pw(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            pw1 = request.POST['new_pw']
            pw2 = request.POST['new_pw_confirm']
            if pw1 == pw2 and request.POST['token'] == request.user.password.split('$')[3].replace('+', ''):
                user = request.user
                user.set_password(pw1)
                user.save()
                return HttpResponse('Your password has been reset. Please close the tab.')
            elif pw1 != pw2:
                return HttpResponse('Your passwords did not match. Hit Back and try again.')
            else:
                #return HttpResponse(f"Token: '{request.POST['token']}' vs '{request.user.password.split('$')[3]}'")
                return HttpResponse('You either got a bad link from Kam or you messed up.')

    else:
        form = NameForm()
        token=request.GET['token']

    return render(request, 'ctl/reset_pw.html', {'form': form, 'token': token})