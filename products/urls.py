from django.urls import path

from products.views import products, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),  # это не тот index, что в url главной папки, это index в products
    # path('category/<int:category_id>/', products, name='category'),  # ../products/category/<id>/
    # path('page/<int:page_number>/', products, name='paginator'),
    path('cat/<int:category_id>/page/<int:page_num>/', products, name='category_paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),  # ../products/baskets/add/<product_id>/
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),  # ../products/baskets/remove/<basket_id>/
]
