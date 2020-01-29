from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
import datetime

from .models import Player, Roster, Game

def index(request):
    return HttpResponse("Index")

def view_elo(request):
    message = ''
    if 'recalculate' not in request.POST:
        players = Player.objects.filter(Q(wins__gte=1) | Q(losses__gte=1)).order_by('-elo')
        return render(request, 'ctlelo/view_elo.html', {'players': players, 'message': message})
    else:
        message = ''
        games = Game.objects.all().order_by('season', 'week')
        players = Player.objects.all()
        for p in players:
            p.reset()
            p.save()
        k = 32 #K FACTOR

        for game in games:
            player1 = game.player1
            player2 = game.player2
            Q_a = 1 + (10 ** (player1.elo/400.0))
            Q_b = 1 + (10 ** (player2.elo/400.0))
            E_a = Q_a / (Q_a+Q_b)
            E_b = Q_b / (Q_a+Q_b)
            p1result = 0
            p2result = 0
            if game.winner == 1:
                p1result = 1
            else:
                p2result = 1
            player1.elo = player1.elo + round(k * (p1result - E_a))
            player2.elo = player2.elo + round(k * (p2result - E_b))
            player1.wins += p1result
            player1.losses += p2result
            player2.wins += p2result
            player2.losses += p1result
            player1.save()
            player2.save()
        players = Player.objects.filter(Q(wins__gte=1) | Q(losses__gte=1)).order_by('-elo')
        return render(request, 'ctlelo/view_elo.html', {'players': players, 'message': message})

def add_game(request):
    return HttpResponse("add_game")

def add_player(request):
    if "name" not in request.POST:
        return render(request, 'ctlelo/add_player.html', {'teams': Roster.objects.all()})
    else:
        name = request.POST['name']
        team = Roster.objects.get(team_name=request.POST['team'])
        league = request.POST['league']
        race = request.POST['race']
        identical_players = Player.objects.filter(name=name)
        if len(identical_players) > 0:
            return render(request, 'ctlelo/add_player.html', {'message': "This could be a duplicate. Add manually if necessary.", 'teams': Roster.objects.all()})
        Player.objects.create(name=name, team=team, league=league, race=race)
        return render(request, 'ctlelo/add_player.html', {'message': "Player added successfully.", 'teams': Roster.objects.all()})


