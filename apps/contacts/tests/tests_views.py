from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker

import swissERP
from apps.contacts.models import Contact
from apps.contacts.views import IndexView, DetailView

faker = Faker()


class ViewsContactsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=faker.name(),
            email=faker.email(),
            password=faker.password()
        )

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_context_object_name(self):
        view = IndexView()
        context_object_name = view.context_object_name
        self.assertTrue(context_object_name, 'contacts_list')

    def test_IndexView_with_filter_request(self):
        for _ in range(10):
            Contact.objects.create(
                user_id=self.user,
                name=faker.first_name(),
                lastname=faker.last_name()
            )
        response1 = self.client.get(reverse("contacts"))
        self.assertEqual(len(response1.context['contacts_list']), 10)

        response2 = self.client.get(reverse("contacts") + '?filter=')
        self.assertEqual(len(response2.context['contacts_list']), 10)

        response3 = self.client.get(reverse("contacts") + '?all=')
        self.assertEqual(len(response3.context['contacts_list']), 10)

        response4 = self.client.get(reverse("contacts") + '?active=')
        self.assertEqual(len(response4.context['contacts_list']), 10)

        response5 = self.client.get(reverse("contacts") + '?archived=')
        self.assertEqual(len(response5.context['contacts_list']), 0)

        x = Contact.objects.get(id=1)
        x.is_active = False
        x.save()

        response6 = self.client.get(reverse("contacts") + '?archived=')
        self.assertEqual(len(response6.context['contacts_list']), 1)

        response7 = self.client.get(reverse("contacts") + '?active=')
        self.assertEqual(len(response7.context['contacts_list']), 9)

        y = Contact.objects.create(
            user_id=self.user,
            name='Fanfan',
            lastname='Noel'
        )

        response8 = self.client.get(reverse("contacts") + '?filter=' + f"{y.name}")
        self.assertEqual(len(response8.context['contacts_list']), 1)

        response9 = self.client.get(reverse("contacts") + '?filter=' + f"{y.lastname}")
        self.assertEqual(len(response9.context['contacts_list']), 1)

    def test_DetailView(self):
        untel = Contact.objects.create(
            user_id=self.user,
            name=faker.first_name(),
            lastname=faker.last_name()
        )
        response = self.client.get(reverse("contact_detail", kwargs={'pk': untel.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contacts_other_infos.html")

        # user logged out
        self.client.logout()
        response = self.client.get(reverse("contact_detail", kwargs={'pk': untel.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f"{swissERP.settings.LOGIN_URL}?next=/contacts/{untel.id}/",
                             status_code=302,
                             target_status_code=200)

    def test_instance_in_DetailView(self):
        view = DetailView()
        self.assertEqual(view.model, Contact)

        for _ in range(3):
            Contact.objects.create(
                user_id=self.user,
                name=faker.first_name(),
                lastname=faker.last_name()
            )
        response = self.client.get(reverse("contact_detail", kwargs={'pk': 2}))
        self.assertIsInstance(response.context['next'], Contact)
        self.assertIsInstance(response.context['previous'], Contact)
        self.assertEqual(response.context['next'].id, 3)
        self.assertEqual(response.context['previous'].id, 1)

