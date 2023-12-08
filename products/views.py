from django.shortcuts import render
from django.http import HttpResponseRedirect
from products.models import ProductCategory, Product, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
# Функции = контроллеры = вьюхи

def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


def products(request, category_id=0, page_num=1):
    products = Product.objects.filter(category_id=category_id).order_by('id') if category_id else Product.objects.all().order_by('id')
    paginator = Paginator(object_list=products, per_page=3)
    products_paginator = paginator.page(number=page_num)
    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
        'selected_cat': category_id
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):  # обработчик событий
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)  # есть ли для этого пользователя этот продукт в корзине

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()  # можно обратиться и last(), все равно у нас это ОДИН товар
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # вернуться на ту же страницу, где были


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
