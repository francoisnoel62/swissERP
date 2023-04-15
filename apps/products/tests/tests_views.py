from django.test import TestCase
from django.urls import reverse
from faker import Faker

from accounts.models import CustomUser
from apps.products.forms import PassModelForm, SubModelForm
from apps.products.models import Product, UnitPass, Subscription
from apps.products.views import ProductListView, ProductDeleteView, ProductCreatePassView, ProductCreateSubView, \
    PassUpdateView, SubscriptionUpdateView
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
                                   price=faker.pyfloat(left_digits=2, right_digits=2, positive=True))

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

    def test_ProductListView_with_filterBy_name(self):
        product_name = "pomme"
        Product.objects.create(created_by=self.user, name=product_name,
                               price=faker.pyfloat(left_digits=2, right_digits=2, positive=True))

        response1 = self.client.get(reverse("products") + '?filter=' + product_name)
        self.assertIsInstance(response1.context['products_list'].first(), Product)
        self.assertTrue(len(response1.context['products_list']) >= 1)
        self.assertEqual(response1.context['products_list'].first().name, product_name)

        # logout
        self.client.logout()
        response4 = self.client.get(reverse("products") + '?filter=' + product_name)
        self.assertEqual(response4.status_code, 302)
        self.assertRedirects(response4,
                             f"{settings.LOGIN_URL}?next=" + reverse("products") + '?filter=' + product_name,
                             status_code=302,
                             target_status_code=200)

    # ProductCreateView
    def test_ProductCreatePassView(self):
        self.assertEqual(ProductCreatePassView().template_name, 'product/create_pass.html')
        self.assertIs(ProductCreatePassView().form_class, PassModelForm)

    def test_ProductCreateSubView(self):
        self.assertEqual(ProductCreateSubView().template_name, 'product/create_subscription.html')
        self.assertIs(ProductCreateSubView().form_class, SubModelForm)

    def test_PassUpdateView(self):
        self.assertEqual(PassUpdateView().template_name, 'product/create_pass.html')
        self.assertIs(PassUpdateView().form_class, PassModelForm)
        self.assertIs(PassUpdateView().model, UnitPass)

        p1 = UnitPass.objects.create(created_by=self.user,
                                    name=faker.text(max_nb_chars=50),
                                    price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                                    remaining_classes=faker.pyint(min_value=1, max_value=10))

        data = {
            'name': 'test',
            'price': 555.9,
            'remaining_classes': 4,
        }

        res1 = self.client.post(
            reverse("edit-pass", kwargs={'pk': p1.id}), data=data)
        self.assertEqual(res1.status_code, 302)
        self.assertRedirects(res1, reverse("products"))
        p1.refresh_from_db()
        self.assertEqual(p1.price, data['price'])
        # self.assertEqual(p1.name, data['name'])

    def test_SubscriptionUpdateView(self):
        self.assertEqual(SubscriptionUpdateView().template_name, 'product/create_subscription.html')
        self.assertIs(SubscriptionUpdateView().form_class, SubModelForm)
        self.assertIs(SubscriptionUpdateView().model, Subscription)

        p1 = Subscription.objects.create(created_by=self.user,
                                    name=faker.text(max_nb_chars=50),
                                    price=faker.pyfloat(left_digits=2, right_digits=2, positive=True),
                                    classes_by_month=faker.pyint(min_value=1, max_value=12))

        data = {
            'name': 'test',
            'price': 555.9,
            'classes_by_month': 4,
        }

        res1 = self.client.post(
            reverse("edit-sub", kwargs={'pk': p1.id}), data=data)
        self.assertEqual(res1.status_code, 302)
        self.assertRedirects(res1, reverse("products"))
        p1.refresh_from_db()
        self.assertEqual(p1.price, data['price'])
        # self.assertEqual(p1.name, data['name'])

    def test_ProductDeleteView(self):
        self.assertIs(ProductDeleteView().model, Product)
        self.assertEqual(ProductDeleteView().success_url, reverse("products"))

        p1 = Product.objects.create(created_by=self.user,
                                    name=faker.text(max_nb_chars=50),
                                    price=faker.pyfloat(left_digits=2, right_digits=2, positive=True))

        res = self.client.post(reverse("delete-product", kwargs={'pk': p1.id}))
        self.assertRedirects(res, reverse("products"), status_code=302)

        res2 = self.client.get(reverse("edit-sub", kwargs={'pk': p1.id}))
        self.assertTrue(res2.status_code, 404)

        res3 = self.client.get(reverse("edit-pass", kwargs={'pk': p1.id}))
        self.assertTrue(res2.status_code, 404)
