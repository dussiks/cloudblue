from rest_framework import viewsets

from .models import Order, OrderDetail, Product
from .serializers import (
    OrderSerializer, OrderDetailSerializer, ProductSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ['external_id', 'status', ]
