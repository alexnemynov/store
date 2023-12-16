from django.http import HttpResponseRedirect
from products.models import ProductCategory, Product, Basket
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = "products"  # Чтобы не использовать в шаблоне "object_list", можно переопределить свойство
    paginate_by = 3
    title = 'Store - Каталог'


    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id', 0)
        return queryset.filter(category_id=category_id) if category_id else queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


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
