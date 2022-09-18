from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker

import swissERP
from apps.contacts.models import Contact
from apps.contacts.views import IndexView

faker = Faker()


class UrlAndTemplatesContactsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=faker.name(),
            email=faker.email(),
            password=faker.password()
        )

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_url_exists_at_correct_location(self):
        # user logged
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 200)

        # user logged out
        self.client.logout()
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 302)

    def test_url_available_by_name(self):
        # user logged
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 302)

    def test_template_name_correct(self):
        # user logged
        response = self.client.get(reverse("contacts"))
        self.assertTemplateUsed(response, "contacts/contacts_listview.html")

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("contacts"))
        self.assertTemplateNotUsed(response, "contacts/contacts_listview.html")

    def test_redirection_if_anonymous_user(self):
        # user logged out
        self.client.logout()
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f"{swissERP.settings.LOGIN_URL}?next=/contacts/",
                             status_code=302,
                             target_status_code=200)






