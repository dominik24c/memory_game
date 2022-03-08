from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import GameRoom, Standings, Game


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
    if search == 'games':
        data = Game.objects.find_all_games()
        type_of_data = 'games'
    elif search == 'player-games':
        data = Game.objects.find_games_by_user(user=user)
        type_of_data = 'player-games'
    else:
        data = Standings.objects.get_all_standings()
        type_of_data = 'standings'

    paginator = Paginator(data, 2)
    page_number = request.GET.get('page')
    data_list = paginator.get_page(page_number)

    context['data'] = data_list
    context['type'] = type_of_data
    return render(request, 'game/index.html', context)


@login_required
def game_view(request: HttpRequest, game_room) -> HttpResponse:
    game_room_obj = GameRoom.objects.filter(id=game_room).first()
    if game_room_obj is not None:
        return render(request, 'game/detail.html', {
            'game_room': game_room
        })
    else:
        return HttpResponseNotFound()
