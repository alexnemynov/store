import uuid

from yookassa import Configuration, Payment

from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect

from .forms import OrderForm
from products.models import Basket


Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    extra_context = {'title': 'Store - Спасибо за заказ!'}


class CancelTemplateView(TemplateView):
    template_name = 'orders/cancel.html'  # заглушка


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    extra_context = {'title': 'Store - Оформление заказа'}

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)  # выполняется логика, которая создает order

        payment = Payment.create({
            'amount': {
                'value': f'{Basket.objects.total_sum()}',
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success'))
            },
            # 'metadata': {'name': name,
            #              'quantity': quantity,
            #              'price': price},
            'capture': True,
            'description': f'Заказ №{self.object.id}'
        }, uuid.uuid4())

        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)  # 303

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


