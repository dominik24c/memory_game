from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class AccountTest(TestCase):
    def test_register(self) -> None:
        credentials = {
            'username': 'test_user',
            'email': 'email@gmail.com',
            'password1': 'Pass1234**',
            'password2': 'Pass1234**'
        }
        response = self.client.post(reverse('auth:signup'), credentials, follow=True)
        body = response.content.decode('utf-8')

        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, credentials['username'])
        self.assertEqual(user.email, credentials['email'])
        self.assertIn(f'<div class="alert">Account was created for {credentials["email"]}</div>', body)

    def test_login(self) -> None:
        credentials = {
            'username': 'test_user',
            'password': 'Pass1234**',
            'email': 'test@test.com'
        }
        user = User.objects.create(
            username=credentials['username'], email=credentials['email'])
        user.set_password(credentials['password'])
        user.save()

        response = self.client.post(reverse('auth:login'), credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, credentials['username'])
        body = response.content.decode('utf-8')
        self.assertIn('<div id="standings">', body)
        self.assertIn('<h3>Standings</h3>', body)
        self.assertIn('<h2>Game</h2>', body)
