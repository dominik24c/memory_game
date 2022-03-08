from django.contrib import admin

# Register your models here.
from .models import GameRoom, Game, Standings

admin.site.register(GameRoom)
admin.site.register(Standings)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'points', 'started_at', 'ended_at')
