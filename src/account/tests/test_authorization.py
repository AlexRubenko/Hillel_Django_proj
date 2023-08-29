from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthCustomer(TestCase):
    def setUp(self) -> None:
        self.client = Client(self)

        self.user = get_user_model().objects.create(email='customer@customer.com')
        self.user.set_password("1234")
        self.user.save()

        self.manager = get_user_model().objects.create(email='someone@someone.com', is_staff=True)
        self.manager.set_password("1234")
        self.manager.save()

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email='wrong_email', password='1234')
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email='customer@customer.com', password='wrong_password')
        self.assertFalse(user_login)

    def test_user_access_admin_panel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin:index'))
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
