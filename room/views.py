from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import GameRoom, Standings, Game


def get_games_or_standings_data(search: str, user=None) -> tuple[QuerySet[Standings] | QuerySet[Game], str]:
    match search:
        case 'games':
            return Game.objects.find_all_games(), 'games'
        case 'player-games':
            return Game.objects.find_games_by_user(user=user), 'player-games'
        case _:
            return Standings.objects.find_all(), 'standings'


@login_required
def game_dashboard_view(request: HttpRequest) -> HttpResponse:
    start_game = request.GET.get('game', '')
    search = request.GET.get('search', '')
    user = request.user

    if start_game == 'start':
        game_room = GameRoom(player=user)
        game_room.save()
        return redirect('game:game', game_room=game_room.id)

    context = {}
    data, type_of_data = get_games_or_standings_data(search, user)

    paginator = Paginator(data, 2)
    page_number = request.GET.get('page')
    data_list = paginator.get_page(page_number)

    context['data'] = data_list
    context['type'] = type_of_data
    return render(request, 'game/dashboard.html', context)


@login_required
def game_view(request: HttpRequest, game_room) -> HttpResponse:
    game_room_obj = GameRoom.objects.filter(id=game_room).first()
    if game_room_obj is not None:
        return render(request, 'game/game.html', {
            'game_room': game_room
        })
    else:
        return HttpResponseNotFound()
