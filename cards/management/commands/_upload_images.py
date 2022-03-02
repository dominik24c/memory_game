import os
from itertools import islice

from django.core.files import File

from ...models import Card


def create_card(file: str, path: str) -> Card:
    card_name = file.replace('.png', '')
    path_to_picture = os.path.join(path, file)
    card = Card.objects.create(name=card_name)
    card.image.save(file, File(open(path_to_picture, 'rb')))
    return card


def upload_image_handler(path: str) -> None:
    Card.objects.all().delete()
    dirs_and_files = os.listdir(path)
    files = list(filter(lambda f: os.path.isfile(os.path.join(path, f)) and f.endswith('.png'), dirs_and_files))
    batch_size = 10
    cards = (create_card(f, path) for f in files)
    while True:
        batch = list(islice(cards, batch_size))
        if not batch:
            break
        Card.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
