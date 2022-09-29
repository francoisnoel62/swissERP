from django.test import TestCase
from django.urls import reverse
from faker import Faker

import swissERP
from accounts.models import CustomUser

faker = Faker()


class UrlAndTemplatesProductsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username=faker.name(),
            email=faker.email(),
            password=faker.password(),
            zip=faker.postcode()
        )

    def setUp(self) -> None:
        self.client.force_login(user=self.user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 302)

    def test_url_available_by_name(self):
        # user logged
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 302)

    def test_template_name_correct(self):
        # user logged
        response = self.client.get(reverse("products"))
        self.assertTemplateUsed(response, "product/products_listview.html")

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("products"))
        self.assertTemplateNotUsed(response, "product/products_listview.html")

    def test_redirection_if_anonymous_user(self):
        # user logged out
        self.client.logout()
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f"{swissERP.settings.LOGIN_URL}?next=/products/",
                             status_code=302,
                             target_status_code=200)


