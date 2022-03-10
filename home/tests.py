from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class HomeTest(TestCase):
    def test_home_view(self) -> None:
        response = self.client.get(reverse('home:home'))
        html = response.content.decode('utf8')
        self.assertIn('<h2>Memory Game!</h2>', html)
