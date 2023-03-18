from PIL.Image import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from accounts.models import CustomUser
from apps.products.models import Product

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
        for _ in range(3):
            Product.objects.create(
                created_by=self.user,
                name=faker.text(max_nb_chars=50),
                price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                description=faker.sentence(),
            )

        self.product1 = Product.objects.get(pk=1)
        self.product2 = Product.objects.get(pk=2)
        self.product3 = Product.objects.get(pk=3)

    def test_product_user_id(self):
        self.assertEqual(self.product1.created_by, self.user)
        self.assertEqual(self.product2.created_by, self.user)
        self.assertEqual(self.product3.created_by, self.user)

    def test_products_absolute_url(self):
        self.assertURLEqual(self.product1.get_absolute_url(), reverse("products"))
