import uuid

from django.db import models


# Create your models here.

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField('cards_images', upload_to='cards')
