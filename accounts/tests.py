from django.test import TestCase, Client
from django.urls import reverse

from faker import Faker

from accounts.models import CustomUser

faker = Faker()


class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username=faker.user_name(),
            email=faker.email(),
            password=faker.password(),
            street=faker.street_address(),
            zip=faker.postcode(),
            city=faker.city(),
            telephone=faker.phone_number()
        )

        self.client = Client()
        self.client.login(username=self.user.username, password=self.user.password)

    def test_get_absolute_url(self):
        url = reverse('home')
        self.assertEqual(self.user.get_absolute_url(), url)

    def test_form_valid(self):
        url = reverse('edit_user', kwargs={'pk': self.user.pk})
        response = self.client.post(url, {'first_name': 'Updated', 'last_name': 'User'})
        self.assertEqual(response.status_code, 302)
