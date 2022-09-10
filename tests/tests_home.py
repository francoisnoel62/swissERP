from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="fanfan",
            email="test@test.ch",
            password="change me!!"
        )

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_url_exists_at_correct_location(self):
        # user logged
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        # user logged out
        self.client.logout()
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 302)

    def test_url_available_by_name(self):
        # user logged
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_template_name_correct(self):
        # user logged
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/home.html")

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertTemplateNotUsed(response, "home/home.html")

    def test_template_content(self):
        # user logged
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<h1>Welcome to swissERP</h1>")

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, "/accounts/login/?next=/home/")
