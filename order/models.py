from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qty_total = models.PositiveIntegerField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('R', 'Rejected'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        )
    )

    def __str__(self):
        return f'Order N. {self.pk}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    id_product = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    id_variation = models.PositiveIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=500)

    def __str__(self):
        return f'Order of {self.order}'
