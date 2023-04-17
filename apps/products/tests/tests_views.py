from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from faker import Faker

from accounts.models import CustomUser
from apps.contacts.models import Contact
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
        self.any_contact = Contact.objects.create(
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

    # ProductListView
    def test_ProductListView_context_object_name(self):
        self.assertEqual(ProductListView().context_object_name, 'products_list')

    def test_ProductListView_login_url(self):
        self.assertEqual(ProductListView().login_url, reverse('login'))

    def test_ProductListView_without_filter(self):
        for _ in range(5):
            Product.objects.create(created_by=self.user,
                                   name=faker.text(max_nb_chars=50),
                                   student=self.any_contact)

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

    # def test_ProductListView_with_filterBy_name(self):
    #     product_name = "pomme"
    #     Product.objects.create(created_by=self.user, name=product_name,
    #                            student=self.any_contact)
    #
    #     response1 = self.client.get(reverse("products") + '?filter=' + product_name)
    #     self.assertIsInstance(response1.context['products_list'].first(), Product)
    #     self.assertTrue(len(response1.context['products_list']) >= 1)
    #     self.assertEqual(response1.context['products_list'].first().name, product_name)
    #
    #     # logout
    #     self.client.logout()
    #     response4 = self.client.get(reverse("products") + '?filter=' + product_name)
    #     self.assertEqual(response4.status_code, 302)
    #     self.assertRedirects(response4,
    #                          f"{settings.LOGIN_URL}?next=" + reverse("products") + '?filter=' + product_name,
    #                          status_code=302,
    #                          target_status_code=200)

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
                                     remaining_classes=faker.pyint(min_value=1, max_value=10),
                                     date_of_buy=faker.date())

        data = {
            'name': 'test',
            'student': self.any_contact.id,
            'remaining_classes': 4,
            'date_of_buy': '2021-01-01',
        }

        res1 = self.client.post(
            reverse("edit-pass", kwargs={'pk': p1.id}), data=data)
        self.assertEqual(res1.status_code, 302)
        self.assertRedirects(res1, reverse("products"))
        p1.refresh_from_db()
        self.assertEqual(p1.name, data['name'])
        self.assertEqual(p1.remaining_classes, data['remaining_classes'])
        self.assertEqual(p1.date_of_buy, datetime(2021, 1, 1).date())

    def test_SubscriptionUpdateView(self):
        self.assertEqual(SubscriptionUpdateView().template_name, 'product/create_subscription.html')
        self.assertIs(SubscriptionUpdateView().form_class, SubModelForm)
        self.assertIs(SubscriptionUpdateView().model, Subscription)

        p1 = Subscription.objects.create(created_by=self.user,
                                         name=faker.text(max_nb_chars=50),
                                         classes_by_week=faker.pyint(min_value=1, max_value=12),
                                         date_of_subscription=faker.date())

        data = {
            'name': 'test',
            'student': self.any_contact.id,
            'classes_by_week': 1,
            'date_of_subscription': '2021-01-01',
            'recurrence': 'M'
        }

        res1 = self.client.post(
            reverse("edit-sub", kwargs={'pk': p1.id}), data=data)
        self.assertEqual(res1.status_code, 302)
        self.assertRedirects(res1, reverse("products"))
        p1.refresh_from_db()

    def test_ProductDeleteView(self):
        self.assertIs(ProductDeleteView().model, Product)
        self.assertEqual(ProductDeleteView().success_url, reverse("products"))

        p1 = Subscription.objects.create(created_by=self.user,
                                         name=faker.text(max_nb_chars=50),
                                         classes_by_week=faker.pyint(min_value=1, max_value=12),
                                         date_of_subscription=faker.date())

        res = self.client.post(reverse("delete-product", kwargs={'pk': p1.id}))
        self.assertRedirects(res, reverse("products"), status_code=302)

        res2 = self.client.get(reverse("edit-sub", kwargs={'pk': p1.id}))
        self.assertTrue(res2.status_code, 404)

        res3 = self.client.get(reverse("edit-pass", kwargs={'pk': p1.id}))
        self.assertTrue(res2.status_code, 404)
