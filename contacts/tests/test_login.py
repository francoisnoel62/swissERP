from http import HTTPStatus

from django.test import Client

from contacts.tests import base_test


class UserLoginTestCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_landing_page(self):
        res = self.client.get('')
        self.assertEquals(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, 'accounts/landing.html')

    def test_anonymous_login(self):
        res = self.client.get('/login/')
        self.assertEquals(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, 'accounts/login.html')

    def test_anonymous_login(self):
        res = self.client.post('/login/', {}, follow=True)
        self.assertEquals(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, 'accounts/register.html')

    def test_user_login(self):
        res = self.client.post('/login/', {
            'username': self.username,
            'password': self.password
        },
                               follow=True)
        self.assertEquals(res.status_code, HTTPStatus.OK)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
