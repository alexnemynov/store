from django.contrib import admin

# Register your models here.
from products.models import ProductCategory, Product, Basket


admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')  # поле отвечает за то, какие поля показать в админке
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')  # какие поля будут по клику. можно на одной строке
    readonly_fields = ('description',)  # какие-то поля только для чтения
    search_fields = ('name',)  # добавить поиск по определенным полям
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):  # несамостоятельная админка, чтобы отобразить в другой админке
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0  # по умолчанию = 3, чтобы дополнительных пустых строчек не выводилось