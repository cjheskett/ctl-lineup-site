from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('add_game', views.add_game, name="add_game"),
    path('view_elo', views.view_elo, name="view_elo"),
    path('add_player_elo', views.add_player, name="add_player_elo"),
]