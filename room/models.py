import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Avg


class GameManager(models.Manager):
    def find_games_by_user(self, user: User) -> QuerySet:
        return self.get_queryset() \
            .select_related('player') \
            .filter(player=user)

    def find_all_games(self) -> QuerySet:
        return self.get_queryset() \
            .select_related('player').all()


class StandingsManager(models.Manager):
    def get_all_standings(self) -> QuerySet:
        return self.get_queryset() \
            .prefetch_related('player', 'player__game') \
            .annotate(points_per_match=Avg('player__game__points')) \
            .only('id', 'points', 'player__username') \
            .all()


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game')
    points = models.IntegerField(default=-1)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)

    objects = GameManager()

    class Meta:
        ordering = ['-ended_at']

    def __str__(self):
        return f'{self.id}'


class GameRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='game_room')
    game = models.OneToOneField(Game, on_delete=models.CASCADE, null=True, related_name='game_room')

    def __str__(self):
        return f'{self.id}'


class Standings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='standings')
    points = models.IntegerField(default=0)

    objects = StandingsManager()

    class Meta:
        ordering = ['-points']
        verbose_name_plural = 'Standings'

    def __str__(self):
        return f'{self.player.username} - {self.points}'
