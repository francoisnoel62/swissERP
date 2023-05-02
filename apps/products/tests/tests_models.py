from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from faker import Faker

from accounts.models import CustomUser
from apps.contacts.models import Contact
from apps.products.models import Subscription, UnitPass

faker = Faker()


class ModelProductsTests(TestCase):
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
        any_contact = Contact.objects.create(
            user_id=self.user,
            is_active=True,
            title=faker.random_element(elements=("Mr", "Ms", "Miss")),
            name=faker.first_name(),
            lastname=faker.last_name(),
            email=faker.email(),
            phone=faker.phone_number(),
            date_of_birth=faker.date(),
            street=faker.street_address(),
            region_zip=faker.postcode(),
            city=faker.city(),
            country=faker.country()
        )

        for _ in range(3):
            Subscription.objects.create(
                user_id=self.user,
                name=faker.text(max_nb_chars=50),
                student=any_contact,
                classes_by_week=1,
                current_credits=1,
                date_of_subscription=faker.date(),
                recurrence=faker.random_element(elements=("M", "A"))
            )

            UnitPass.objects.create(
                user_id=self.user,
                name=faker.text(max_nb_chars=50),
                student=any_contact,
                remaining_classes=faker.random_int(min=1, max=10),
                date_of_buy=faker.date()
            )

        self.sub1 = Subscription.objects.get(pk=1)
        self.sub2 = Subscription.objects.get(pk=3)
        self.sub3 = Subscription.objects.get(pk=5)

        self.pass1 = UnitPass.objects.get(pk=2)
        self.pass2 = UnitPass.objects.get(pk=4)
        self.pass3 = UnitPass.objects.get(pk=6)

    def test_product_user_id(self):
        self.assertEqual(self.sub1.user_id, self.user)
        self.assertEqual(self.sub2.user_id, self.user)
        self.assertEqual(self.sub3.user_id, self.user)

        self.assertEqual(self.pass1.user_id, self.user)
        self.assertEqual(self.pass2.user_id, self.user)
        self.assertEqual(self.pass3.user_id, self.user)

    def test_products_absolute_url(self):
        self.assertURLEqual(self.sub1.get_absolute_url(), reverse("products"))
        self.assertURLEqual(self.sub2.get_absolute_url(), reverse("products"))
        self.assertURLEqual(self.sub2.get_absolute_url(), reverse("products"))

        self.assertURLEqual(self.pass1.get_absolute_url(), reverse("products"))
        self.assertURLEqual(self.pass2.get_absolute_url(), reverse("products"))
        self.assertURLEqual(self.pass2.get_absolute_url(), reverse("products"))

    def test_product_name(self):
        self.assertEqual(self.sub1.__str__(), f"{self.sub1.name} - {self.sub1.student}")
        self.assertEqual(self.sub2.__str__(), f"{self.sub2.name} - {self.sub2.student}")
        self.assertEqual(self.sub3.__str__(), f"{self.sub3.name} - {self.sub3.student}")

        self.assertEqual(self.pass1.__str__(), f"{self.pass1.name} - {self.pass1.student}")
        self.assertEqual(self.pass2.__str__(), f"{self.pass2.name} - {self.pass2.student}")
        self.assertEqual(self.pass3.__str__(), f"{self.pass3.name} - {self.pass3.student}")

    def test_subscription_date_of_renewal(self):
        self.sub4 = Subscription.objects.create(
            user_id=self.user,
            name=faker.text(max_nb_chars=50),
            student=self.sub1.student,
            classes_by_week=1,
            current_credits=1,
            date_of_subscription="2021-01-01",
            recurrence="A"
        )

        self.assertEqual(self.sub4.date_of_renewal, datetime(2022, 1, 1))

        self.sub4.recurrence = "M"
        self.sub4.save()

        self.assertEqual(self.sub4.date_of_renewal, datetime(2021, 2, 1))

    def test_unipass_end_of_validity(self):
        self.pass4 = UnitPass.objects.create(
            user_id=self.user,
            name=faker.text(max_nb_chars=50),
            student=self.pass1.student,
            remaining_classes=faker.random_int(min=1, max=10),
            date_of_buy="2021-01-01"
        )

        self.assertEqual(self.pass4.end_of_validity, datetime(2022, 1, 1))
