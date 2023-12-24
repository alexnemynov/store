from django.db import models

from users.models import User


class Order(models.Model):
    CREATED = 0  # Статусы указывают в начале класса
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)  # нельзя ссылаться на другие модели, чтобы поле не обновлялась
    created = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(choices=STATUSES, default=CREATED)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)  # если удалился пользователь, и заказа тоже удаляем

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'


