from django.shortcuts import render

# Create your views here.
# Функции = контроллеры = вьюхи

def index(request):
    return render(request, 'products/index.html')


def products(request):
    return render(request, 'products/products.html')