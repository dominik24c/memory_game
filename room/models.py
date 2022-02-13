import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class GameRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(default=0)
