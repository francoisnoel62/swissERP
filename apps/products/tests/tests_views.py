from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from accounts.models import CustomUser
from apps.products.forms import ProductModelForm
from apps.products.models import Product
from apps.products.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
from swissERP import settings

faker = Faker()


class ViewsProductsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username=faker.name(), email=faker.email(), password=faker.password(),
                                                  zip=faker.postcode())

    def setUp(self) -> None:
        self.client.force_login(user=self.user)

    # ProductListView
    def test_ProductListView_context_object_name(self):
        self.assertEqual(ProductListView().context_object_name, 'products_list')

    def test_ProductListView_login_url(self):
        self.assertEqual(ProductListView().login_url, reverse('login'))

    def test_ProductListView_without_filter(self):
        for _ in range(5):
            Product.objects.create(created_by=self.user,
                                   name=faker.text(max_nb_chars=50),
                                   price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                                   description=faker.sentence(),
                                   picture=SimpleUploadedFile(name='test_image.jpg',
                                                              content=b'',
                                                              content_type='image/jpeg'))

        response1 = self.client.get(reverse("products"))
        self.assertEqual(len(response1.context['products_list']), 5)

        response2 = self.client.get(reverse("products") + '?filter=')
        self.assertEqual(len(response2.context['products_list']), 5)

        # logout
        self.client.logout()
        response1 = self.client.get(reverse("products"))
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, f"{settings.LOGIN_URL}?next=" + reverse("products"))

        response2 = self.client.get(reverse("products") + '?filter=')
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2,
                             f"{settings.LOGIN_URL}?next=" + reverse("products") + '?filter=',
                             status_code=302,
                             target_status_code=200)

    def test_ProductListView_with_filterBy_name_or_desc(self):
        product_name = "pomme"
        product_desc = "une pomme très sucrée"
        Product.objects.create(created_by=self.user, name=product_name,
                               price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                               description=product_desc,
                               picture=SimpleUploadedFile(name='test_image.jpg', content=b'',
                                                          content_type='image/jpeg'))

        response1 = self.client.get(reverse("products") + '?filter=' + product_name)
        self.assertIsInstance(response1.context['products_list'].first(), Product)
        self.assertTrue(len(response1.context['products_list']) >= 1)
        self.assertEqual(response1.context['products_list'].first().name, product_name)
        self.assertEqual(response1.context['products_list'].first().description, product_desc)

        response2 = self.client.get(reverse("products") + '?filter=' + product_desc)
        self.assertIsInstance(response2.context['products_list'].first(), Product)
        self.assertTrue(len(response2.context['products_list']) >= 1)
        self.assertEqual(response2.context['products_list'].first().name, product_name)
        self.assertEqual(response2.context['products_list'].first().description, product_desc)

        response3 = self.client.get(reverse("products") + '?filter=' + "sucrée")
        self.assertIsInstance(response3.context['products_list'].first(), Product)
        self.assertTrue(len(response3.context['products_list']) >= 1)
        self.assertEqual(response3.context['products_list'].first().name, product_name)
        self.assertEqual(response3.context['products_list'].first().description, product_desc)

        # logout
        self.client.logout()
        response4 = self.client.get(reverse("products") + '?filter=' + product_name)
        self.assertEqual(response4.status_code, 302)
        self.assertRedirects(response4,
                             f"{settings.LOGIN_URL}?next=" + reverse("products") + '?filter=' + product_name,
                             status_code=302,
                             target_status_code=200)

    # ProductCreateView
    def test_ProductCreateView(self):
        self.assertEqual(ProductCreateView().template_name, 'product/create_product.html')
        self.assertIs(ProductCreateView().form_class, ProductModelForm)

    def test_ProductUpdateView(self):
        self.assertEqual(ProductUpdateView().template_name, 'product/create_product.html')
        self.assertIs(ProductUpdateView().form_class, ProductModelForm)
        self.assertIs(ProductUpdateView().model, Product)

        p1 = Product.objects.create(created_by=self.user,
                                    name=faker.text(max_nb_chars=50),
                                    price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                                    description=faker.sentence(),
                                    picture=SimpleUploadedFile(name='test_image.jpg',
                                                               content=b'',
                                                               content_type='image/jpeg'))

        data = {
            'name': 'test',
            'price': 555.9,
            'description': 'desc',
        }

        res1 = self.client.post(
            reverse("edit-product", kwargs={'pk': p1.id}), data=data)
        self.assertEqual(res1.status_code, 302)
        self.assertRedirects(res1, reverse("products"))
        p1.refresh_from_db()
        self.assertEqual(p1.price, data['price'])
        self.assertEqual(p1.name, data['name'])
        self.assertEqual(p1.description, data['description'])

    def test_ProductDeleteView(self):
        self.assertIs(ProductDeleteView().model, Product)
        self.assertEqual(ProductDeleteView().success_url, reverse("products"))

        p1 = Product.objects.create(created_by=self.user,
                                    name=faker.text(max_nb_chars=50),
                                    price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                                    description=faker.sentence(),
                                    picture=SimpleUploadedFile(name='test_image.jpg',
                                                               content=b'',
                                                               content_type='image/jpeg'))

        res = self.client.post(reverse("delete-product", kwargs={'pk': p1.id}))
        self.assertRedirects(res, reverse("products"), status_code=302)

        res2 = self.client.get(reverse("edit-product", kwargs={'pk': p1.id}))
        self.assertTrue(res2.status_code, 404)
