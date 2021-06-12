from django.db import models


class Status(models.TextChoices):
    NEW = 'new', 'New'
    ACCEPTED = 'accepted', 'Accepted'
    FAILED = 'failed', 'Failed'


class Order(models.Model):
    status = models.CharField(
        'Status',
        max_length=12,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField('Creation date', auto_now_add=True)
    external_id = models.CharField('External identifier', max_length=128)

    class Meta:
        ordering = ('id', 'status', 'external_id',)

    def __str__(self):
        return f'order id_{self.id}'


class Product(models.Model):
    name = models.CharField('Product', max_length=64, unique=True)

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='details',
    )
    amount = models.IntegerField('Amount')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='details',
    )
    price = models.DecimalField(
        'Price',
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return f'{self.order}_details'
