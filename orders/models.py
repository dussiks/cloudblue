from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(
        'Status',
        max_length=12,
        choices=STATUS_CHOICES,
        default='new',
    )
    created_at = models.DateTimeField('Creation date', auto_now_add=True)
    external_id = models.CharField('External identifier', max_length=128)

    class Meta:
        ordering = ('id', 'status', 'external_id',)

    def __str__(self):
        return f'order id_{self.id}'


class Product(models.Model):
    name = models.CharField('Product', max_length=64)

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='details',
        null=False,
        blank=False,
    )
    amount = models.IntegerField('Amount')
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='details',
        blank=False,
        null=True,
    )
    price = models.DecimalField('Price', max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.order}_details'
