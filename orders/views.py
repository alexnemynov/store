import uuid
import json

from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm
from products.models import Basket
from .models import Order

Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    extra_context = {'title': 'Store - Спасибо за заказ!'}


class CancelTemplateView(TemplateView):
    template_name = 'orders/cancel.html'  # заглушка


class OrderListView(ListView):
    template_name = 'orders/orders.html'
    extra_context = {'title': 'Store - Заказы'}
    context_object_name = "orders"  # Чтобы не использовать в шаблоне "object_list"
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    extra_context = {'title': 'Store - Оформление заказа'}

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)  # выполняется логика, которая создает order
        baskets = Basket.objects.filter(user=self.request.user)

        payment = Payment.create({
            'amount': {
                'value': f'{baskets.total_sum()}',
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success'))
            },
            'metadata': {'order_id': self.object.id},
            'capture': True,
            'description': f'Заказ №{self.object.id}'
        }, uuid.uuid4())

        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)  # 303

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt  # данный декоратор убирает необходимость того, что нужно передавать csrf токен
def yookassa_webhook_view(request):
    # Извлечение JSON объекта из тела запроса
    event_json = json.loads(request.body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object   # Получите объект платежа
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            session = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
                'metadata': response_object.metadata
            }
            fullfill_order(session)

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика

        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            some_data = {
                'refundId': response_object.id,
                'refundStatus': response_object.status,
                'paymentId': response_object.payment_id,
            }
            # Специфичная логика

        elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
            some_data = {
                'dealId': response_object.id,
                'dealStatus': response_object.status,
            }
            # Специфичная логика

        elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика

        elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика

        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    except Exception:
        # Обработка ошибок
        return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо


def fullfill_order(session):
    order_id = session['metadata']['order_id']
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
