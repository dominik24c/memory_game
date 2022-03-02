from django.urls import path

from .views import game_dashboard_view, game_view

app_name = 'game'

urlpatterns = [
    path('', game_dashboard_view, name='dashboard'),
    path('<str:game_room>/', game_view, name='game'),
]
