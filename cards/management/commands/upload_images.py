from django.conf import settings
from django.core.management.base import BaseCommand

from ._upload_images import upload_image_handler


class Command(BaseCommand):
    help = 'Upload cards images to database.'

    def handle(self, *args, **options):
        upload_image_handler(settings.CARDS_IMG_DIR)
        self.stdout.write('Card images was saved!')
