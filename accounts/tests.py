from django.test import TestCase
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

    def test_get_absolute_url(self):
        url = reverse('home')
        self.assertEqual(self.user.get_absolute_url(), url)
