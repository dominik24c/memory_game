import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from .models import Card


# Create your tests here.

class CardCommandTest(TestCase):
    def test_upload_cards(self) -> None:
        call_command('upload_images')
        card_count = Card.objects.count()
        dirs_and_files = os.listdir(settings.CARDS_IMG_DIR)
        files = list(filter(lambda f: os.path.isfile(os.path.join(settings.CARDS_IMG_DIR, f))
                                      and f.endswith('.png'), dirs_and_files))
        self.assertEqual(card_count, len(files))
