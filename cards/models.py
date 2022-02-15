import uuid

from django.db import models


# Create your models here.

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='cards', height_field='128', width_field='128')
