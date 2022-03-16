from django.db import models

from products.models import Product


class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return f'{self.id} - {self.date_time}'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return f'{self.id} - {self.order} - {self.product}'