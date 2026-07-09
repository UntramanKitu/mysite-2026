from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class ProductsPageTests(TestCase):
    def test_products_page_shows_mock_products_when_database_is_empty(self):
        response = self.client.get(reverse('chopee:products_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15')
        self.assertContains(response, 'Sữa rửa mặt')

    def test_profile_page_is_available_for_authenticated_user(self):
        user = User.objects.create_user(username='tester', password='secret123')
        self.client.login(username='tester', password='secret123')

        response = self.client.get(reverse('chopee:user_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'โปรไฟล์ของฉัน')
