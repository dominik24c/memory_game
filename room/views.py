from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def game(request: HttpRequest) -> HttpResponse:
    return render(request, 'game/index.html')
