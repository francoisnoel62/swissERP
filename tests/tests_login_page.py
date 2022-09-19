from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from faker import Faker

from accounts.models import CustomUser

faker = Faker()


class LoginPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username=faker.name(),
            email=faker.email(),
            password=faker.password(),
            zip=faker.postcode()
        )

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "registration/login.html")

    def test_template_content(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "<p class=\"h4 mb-4\">Sign in</p>")

    def test_already_user_redirection(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("home"), status_code=302, target_status_code=200)

