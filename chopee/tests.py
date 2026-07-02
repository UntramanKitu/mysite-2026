from django.test import TestCase
from django.urls import reverse


class ProductsPageTests(TestCase):
    def test_products_page_shows_mock_products_when_database_is_empty(self):
        response = self.client.get(reverse('chopee:products_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15')
        self.assertContains(response, 'Sữa rửa mặt')
