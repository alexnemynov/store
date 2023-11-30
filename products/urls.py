from django.urls import path

from products.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),  # это не тот index, что в url главной папки, это index в products
]
