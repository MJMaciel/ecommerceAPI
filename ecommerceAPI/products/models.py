import uuid

from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=20)
    stock = models.PositiveIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0.1)])

    def __str__(self):
        return f'{self.id} - {self.name}'