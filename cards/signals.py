from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Card


@receiver(pre_delete, sender=Card)
def pre_delete_card_handler(instance: Card, sender, *args, **kwargs) -> None:
    instance.image.storage.delete(instance.image.name)
