from django import setup
setup()

from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')  # http //127.0.0.1:8000/
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # сравниваем приходящий код HTTP и код 200
        self.assertEqual(response.context_data['title'], 'Store')  # какой заголовок используется
        self.assertTemplateUsed(response, 'products/index.html')  # какой шаблон используется

