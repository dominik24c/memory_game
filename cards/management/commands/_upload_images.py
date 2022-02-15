import os
from itertools import islice

from PIL import Image
from django.conf import settings

from ...models import Card


def upload_image_handler(path: str) -> None:
    dirs_and_files = os.listdir(path)
    files = list(filter(lambda f: os.path.isfile(os.path.join(path, f)) and f.endswith('.png'), dirs_and_files))
    batch_size = 10
    cards = (Card(name=f.replace('.png', ''), image=Image.open(settings.BASE_DIR / f)) for f in files)
    while True:
        batch = list(islice(cards, batch_size))
        if not batch:
            break
        Card.objects.bulk_create(batch, batch_size)
