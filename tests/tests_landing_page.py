from django.test import SimpleTestCase
from django.urls import reverse


class LandingPageTest(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("landing"))
        self.assertTemplateUsed(response, "home/landing.html")

    def test_template_content(self):
        response = self.client.get(reverse("landing"))
        self.assertContains(response, "<title>circa+ Free Business Software</title>")
