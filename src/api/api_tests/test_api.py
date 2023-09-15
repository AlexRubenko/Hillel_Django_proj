from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from document_flow.models import Project


class CustomerTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.com', password='test123', role='manager')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def _get_auth_headers(self):
        return {
            "HTTP_AUTHORIZATION": f"Bearer {self.access_token}"
        }

    def test_create_customer(self):
        url = reverse('api:customers-list')
        data = {
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'email': 'customer@test.com',
            'is_staff': False,
            'role': 'manager',  # Или другое значение, зависящее от выбора
            'phone_number': '+380991234567',
            'is_active': True,
            'access_status': 'view',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json', **self._get_auth_headers())
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_update_customer(self):
        url = reverse('api:customer_update', args=[self.user.pk])
        data = {
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLastName',
            'email': 'updated_email@test.com',
            'is_staff': True,
            'role': 'engineer',
            'phone_number': '+380991234567',
            'is_active': False,
            'access_status': 'edit'
        }
        response = self.client.put(url, data, format='json', **self._get_auth_headers())
        if response.status_code != status.HTTP_200_OK:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedName')

    def test_delete_customer(self):
        url = reverse('api:customer_delete', args=[self.user.pk])
        response = self.client.delete(url, **self._get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_list_caddocuments(self):
        url = reverse('api:caddocuments_list')
        response = self.client.get(url, **self._get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project_detail(self):
        project = Project.objects.create(name="TestProject", project_number="123-123")
        url = reverse('api:project-detail', args=[project.pk])
        response = self.client.get(url, **self._get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
