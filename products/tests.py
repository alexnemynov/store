# from django import setup
# setup()

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')  # http //127.0.0.1:8000/
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # сравниваем приходящий код HTTP и код 200
        self.assertEqual(response.context_data['title'], 'Store')  # какой заголовок используется
        self.assertTemplateUsed(response, 'products/index.html')  # какой шаблон используется


class ProdcutsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):  # обьявляем тут переменные, необходимые в тестах
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self.__common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category_paginator', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self.__common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def __common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
