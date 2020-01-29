from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('roster_test', views.roster_test, name='roster_test'),
    path('pet_duck', views.pet_duck, name='pet_duck'),
    path('<str:team>/bulk_add', views.bulk_add, name='bulk_add'),
    path('submit_lineup', views.submit_lineup, name="submit_lineup"),
    path('create_typeform', views.create_typeform, name="create_typeform"),
    path('typeform', views.typeform, name='typeform'),
    path('add_player', views.add_player, name='add_player'),
    path('edit_player', views.edit_player, name='edit_player'),
    path('create_account', views.create_account, name='create_account'),
    path('remove_player', views.remove_player, name='remove_player'),
    path('view_lineups', views.view_lineups, name='view_lineups'),
    path('css_test', views.css_test, name='css_test'),
    path('submit_match_report', views.submit_match_report, name='submit_match_report'),
    path('view_match_reports', views.view_match_reports, name='view_match_reports'),
    path('view_lineups_blank', views.view_lineups_blank, name='view_lineups_blank'),
    path('reset_pw', views.reset_pw, name='reset_pw'),
]