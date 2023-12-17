from .models import Basket


def baskets(request):  # название глобальной переменной, к которой мы будем обращаться
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
