from django.db import models

from users.models import User  # чтобы использовать Foreign Key


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)  # макс длина в символах; поля уникальны
    description = models.TextField(null=True, blank=True)  # 2 способа задать пуст стр; поле Discription мож быть пустым

    class Meta:
        verbose_name = 'Category'  # наименование модели в админке
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()  # поле обязательно к заполнению
    price = models.DecimalField(max_digits=8, decimal_places=2)  # всего цифр; цифр после запятой
    quantity = models.PositiveIntegerField(default=0)  # только положительные значения; по умолчанию 0
    image = models.ImageField(upload_to='products_images')  # папка для сохранения изображений
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)  # ссылка на внешний ключ; каск удаление

    class Meta:
        verbose_name = 'Product'  # наименование модели в админке
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'продукт: {self.name} | Категория: {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)  # дата обновляется автоматически при создании обьекта

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }

        return basket_item
