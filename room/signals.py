from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.signals import (post_save, post_delete)
from django.dispatch import receiver

from .models import GameRoom, Game, Standings


@receiver(post_save, sender=GameRoom)
def post_save_game_room_handler(sender, instance, created, *args, **kwargs) -> None:
    if created:
        game = Game.objects.create(player=instance.player)
        instance.game = game
        instance.save()


@receiver(post_save, sender=User)
def post_save_user_handler(sender, instance, created, *args, **kwargs) -> None:
    if created:
        Standings.objects.create(player=instance)


@receiver(post_save, sender=Game)
def post_save_game_handler(sender, instance, created, *args, **kwargs) -> None:
    if not created:
        standings = Standings.objects.filter(player=instance.player).first()
        standings.points = F('points') + instance.points
        standings.save()


@receiver(post_delete, sender=Game)
def post_delete_game_handler(sender, instance, *args, **kwargs) -> None:
    standings = Standings.objects.filter(player=instance.player).first()
    standings.points = F('points') - instance.points
    standings.save()
