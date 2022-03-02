from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import GameRoom


def game_dashboard_view(request: HttpRequest) -> HttpResponse:
    start_game = request.GET.get('game', '')
    if start_game == 'start':
        user = request.user
        game_room = GameRoom(player=user)
        game_room.save()
        return redirect('game:game', game_room=game_room.id)
    return render(request, 'game/index.html')


def game_view(request: HttpRequest, game_room) -> HttpResponse:
    game_room_obj = GameRoom.objects.prefetch_related('player')\
                    .filter(id=game_room).first()
    if game_room_obj is not None:
        player_id = game_room_obj.player.id
        if player_id == request.user.id:
            return render(request, 'game/detail.html', {
                'game_room': game_room
            })
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return HttpResponseNotFound()
