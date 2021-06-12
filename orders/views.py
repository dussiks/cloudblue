from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Status, Order, OrderDetail, Product
from .serializers import (
    OrderSerializer, OrderDetailSerializer, ProductSerializer
)


NOT_NEW_ORDER_STATUS_TEXT = 'Only "new" status of order could be changed.'


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ['external_id', 'status', ]

    @action(detail=True, methods=['post'], url_path='accept')
    def change_status_to_accepted(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                f'No object with id={pk} found',
                status=status.HTTP_400_BAD_REQUEST
            )
        if order.status == Status.NEW:
            order.status = Status.ACCEPTED
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            NOT_NEW_ORDER_STATUS_TEXT,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=['post'], url_path='fail')
    def change_status_to_failed(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                f'No object with id={pk} found',
                status=status.HTTP_400_BAD_REQUEST
            )
        if order.status == Status.NEW:
            order.status = Status.FAILED
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            NOT_NEW_ORDER_STATUS_TEXT,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

