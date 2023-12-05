from django.db import models

from users.models import User  # чтобы использовать Foreign Key

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)  # макс длина в символах; поля уникальны
    description = models.TextField(null=True, blank=True)  # два способа задать пуст стр; поле Discription может быть пустым

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()  # поле обязательно к заполнению
    price = models.DecimalField(max_digits=8, decimal_places=2)  # всего цифр; цифр после запятой
    quantity = models.PositiveIntegerField(default=0)  # только положительные значения; по умолчанию 0
    image = models.ImageField(upload_to='products_images')  # папка для сохранения изображений
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)  # ссылка на внешний ключ; каскадное удаление

    def __str__(self):
        return f'продукт: {self.name} | Категория: {self.category.name}'


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)  # дата обновляется автоматически при создании нового обьекта

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'