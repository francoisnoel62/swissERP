from contacts.tests import base_test
from django.test import Client


class UserLoginTestCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()

    def test_user_login(self):
        client = Client()
        res = client.post('/login/', {
            'username': self.username,
            'password': self.password
        },
                          follow=True)

        self.assertEquals(res.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
