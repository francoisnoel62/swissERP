from django.urls import reverse
from faker import Faker
from accounts.models import CustomUser

from django.test import TestCase

from apps.contacts.models import Contact

faker = Faker()


class ModelContactsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username=faker.name(),
            email=faker.email(),
            password=faker.password(),
            zip=faker.postcode()
        )

    def setUp(self):
        self.client.force_login(user=self.user)
        self.contact1 = Contact.objects.create(
            user_id=self.user,
            name=faker.first_name(),
            lastname=faker.last_name(),
        )

    def test_contact_user_id(self):
        self.assertEqual(self.contact1.user_id, self.user)

    def test_contact_active(self):
        self.assertEqual(self.contact1.is_active, True)

    def test_contact_title(self):
        self.assertEqual(self.contact1.title, "Mme")

    def test_contact_lang(self):
        self.assertEqual(self.contact1.lang, "US")

    def test_contact_country(self):
        self.assertEqual(self.contact1.country, "CH")

    def test_contact_absolute_url(self):
        self.assertURLEqual(self.contact1.get_absolute_url(), reverse('contact_detail', kwargs={'pk': self.contact1.id}))

    def test_contact_title(self):
        self.assertEqual(self.contact1.title, "Mme")

    def test_contact_str_method(self):
        self.assertEqual(str(self.contact1), f"{self.contact1.name} {self.contact1.lastname}")